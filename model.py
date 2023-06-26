import torch
import torch.nn as nn


class ResnetBlock(nn.Module):
    def __init__(self, channels_n):
        super(ResnetBlock, self).__init__()
        self.conv_block = nn.Sequential(
            nn.ReflectionPad2d((1, 1, 1, 1)),
            nn.Conv2d(channels_n, channels_n,
                      kernel_size=(3, 3), stride=(1, 1)),
            nn.InstanceNorm2d(channels_n, eps=1e-5, momentum=0.1,
                              affine=False, track_running_stats=False),
            nn.ReLU(inplace=True),
            nn.ReflectionPad2d((1, 1, 1, 1)),
            nn.Conv2d(channels_n, channels_n,
                      kernel_size=(3, 3), stride=(1, 1)),
            nn.InstanceNorm2d(channels_n, eps=1e-5, momentum=0.1,
                              affine=False, track_running_stats=False),
        )

    def forward(self, x):
        return x + self.conv_block(x)


class ResnetGenerator(nn.Module):
    def __init__(self):
        super(ResnetGenerator, self).__init__()
        self.model = []
        self.downsampler = [
            nn.ReflectionPad2d((3, 3, 3, 3)),
            nn.Conv2d(3, 64, kernel_size=(7, 7), stride=(1, 1)),
            nn.InstanceNorm2d(64, eps=1e-05, momentum=0.1,
                              affine=False, track_running_stats=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=(3, 3),
                      stride=(2, 2), padding=(1, 1)),
            nn.InstanceNorm2d(128, eps=1e-05, momentum=0.1,
                              affine=False, track_running_stats=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 256, kernel_size=(3, 3),
                      stride=(2, 2), padding=(1, 1)),
            nn.InstanceNorm2d(256, eps=1e-05, momentum=0.1,
                              affine=False, track_running_stats=False),
            nn.ReLU(inplace=True),
        ]
        self.transformer = [ResnetBlock(256) for _ in range(9)]
        self.upsampler = [
            nn.ConvTranspose2d(256, 128, kernel_size=(3, 3), stride=(
                2, 2), padding=(1, 1), output_padding=(1, 1)),
            nn.InstanceNorm2d(128, eps=1e-05, momentum=0.1,
                              affine=False, track_running_stats=False),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, kernel_size=(3, 3), stride=(
                2, 2), padding=(1, 1), output_padding=(1, 1)),
            nn.InstanceNorm2d(64, eps=1e-05, momentum=0.1,
                              affine=False, track_running_stats=False),
            nn.ReLU(inplace=True),
            nn.ReflectionPad2d((3, 3, 3, 3)),
            nn.Conv2d(64, 3, kernel_size=(7, 7), stride=(1, 1)),
            nn.Tanh()
        ]
        self.model = self.downsampler + self.transformer + self.upsampler
        self.model = nn.Sequential(*self.model)

    def forward(self, x):
        return self.model(x)

    def __patch_instance_norm_state_dict(self, state_dict, module, keys, i=0):
        """Fix InstanceNorm checkpoints incompatibility (prior to 0.4)"""
        key = keys[i]
        if i + 1 == len(keys):  # at the end, pointing to a parameter/buffer
            if module.__class__.__name__.startswith('InstanceNorm') and \
                    (key == 'running_mean' or key == 'running_var'):
                if getattr(module, key) is None:
                    state_dict.pop('.'.join(keys))
            if module.__class__.__name__.startswith('InstanceNorm') and \
               (key == 'num_batches_tracked'):
                state_dict.pop('.'.join(keys))
        else:
            self.__patch_instance_norm_state_dict(state_dict, getattr(module, key), keys, i + 1)

    def load_networks(self, model_path):
        net = self
        print('loading the model from %s' % model_path)
        # if you are using PyTorch newer than 0.4 (e.g., built from
        # GitHub source), you can remove str() on self.device
        state_dict = torch.load(model_path)
        if hasattr(state_dict, '_metadata'):
            del state_dict._metadata

        # patch InstanceNorm checkpoints prior to 0.4
        for key in list(state_dict.keys()):  # need to copy keys here because we mutate in loop
            self.__patch_instance_norm_state_dict(state_dict, net, key.split('.'))
        net.load_state_dict(state_dict)

