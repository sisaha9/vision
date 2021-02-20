from .._utils import IntermediateLayerGetter
from ..utils import load_state_dict_from_url
from .. import resnet
from .deeplabv3 import DeepLabHead, DeepLabV3
from .fcn import FCN, FCNHead


#FCN_Resnet18 and FCN_Resnet34 added from https://github.com/dusty-nv/vision/tree/v0.3.0
__all__ = ['fcn_resnet18', 'fcn_resnet34', 'fcn_resnet50', 'fcn_resnet101', 'deeplabv3_resnet50', 'deeplabv3_resnet101']


#FCN_Resnet18 and FCN_Resnet34 added from https://github.com/dusty-nv/vision/tree/v0.3.0
model_urls = {
    'fcn_resnet18_coco': None,
    'fcn_resnet34_coco': None,
    'fcn_resnet50_coco': 'https://download.pytorch.org/models/fcn_resnet50_coco-1167a1af.pth',
    'fcn_resnet101_coco': 'https://download.pytorch.org/models/fcn_resnet101_coco-7ecb50ca.pth',
    'deeplabv3_resnet50_coco': 'https://download.pytorch.org/models/deeplabv3_resnet50_coco-cd0a2569.pth',
    'deeplabv3_resnet101_coco': 'https://download.pytorch.org/models/deeplabv3_resnet101_coco-586e9e4e.pth',
}


def _segm_resnet(name, backbone_name, num_classes, aux, pretrained_backbone=True, export_onnx=False):
    if backbone_name == "resnet18" or backbone_name == "resnet34":
        replace_stride_with_dilation=[False, False, False]
        inplanes_scale_factor = 4
    else:
        replace_stride_with_dilation=[False, True, True]
        inplanes_scale_factor = 1

    backbone = resnet.__dict__[backbone_name](
        pretrained=pretrained_backbone,
        replace_stride_with_dilation=replace_stride_with_dilation)

    return_layers = {'layer4': 'out'}
    if aux:
        return_layers['layer3'] = 'aux'
    backbone = IntermediateLayerGetter(backbone, return_layers=return_layers)

    aux_classifier = None
    if aux:
        inplanes = int(1024 / inplanes_scale_factor)
        aux_classifier = FCNHead(inplanes, num_classes)

    model_map = {
        'deeplabv3': (DeepLabHead, DeepLabV3),
        'fcn': (FCNHead, FCN),
    }
    inplanes = int(2048 / inplanes_scale_factor)
    classifier = model_map[name][0](inplanes, num_classes)
    base_model = model_map[name][1]

    model = base_model(backbone, classifier, aux_classifier, export_onnx)
    return model


def _load_model(arch_type, backbone, pretrained, progress, num_classes, aux_loss, **kwargs):
    print(f'torchvision.models.segmentation.{arch_type}_{backbone}()')
    if pretrained:
        aux_loss = True
    model = _segm_resnet(arch_type, backbone, num_classes, aux_loss, **kwargs)
    if pretrained:
        arch = arch_type + '_' + backbone + '_coco'
        model_url = model_urls[arch]
        if model_url is None:
            raise NotImplementedError('pretrained {} is not supported as of now'.format(arch))
        else:
            state_dict = load_state_dict_from_url(model_url, progress=progress)
            model.load_state_dict(state_dict)
    return model

def fcn_resnet18(pretrained=False, progress=True,
                 num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-18 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet18', pretrained, progress, num_classes, aux_loss, **kwargs)

def fcn_resnet34(pretrained=False, progress=True,
                 num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-34 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet34', pretrained, progress, num_classes, aux_loss, **kwargs)

def fcn_resnet50(pretrained=False, progress=True,
                 num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-50 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet50', pretrained, progress, num_classes, aux_loss, **kwargs)


def fcn_resnet101(pretrained=False, progress=True,
                  num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-101 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet101', pretrained, progress, num_classes, aux_loss, **kwargs)


def deeplabv3_resnet50(pretrained=False, progress=True,
                       num_classes=21, aux_loss=None, **kwargs):
    """Constructs a DeepLabV3 model with a ResNet-50 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('deeplabv3', 'resnet50', pretrained, progress, num_classes, aux_loss, **kwargs)


def deeplabv3_resnet101(pretrained=False, progress=True,
                        num_classes=21, aux_loss=None, **kwargs):
    """Constructs a DeepLabV3 model with a ResNet-101 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('deeplabv3', 'resnet101', pretrained, progress, num_classes, aux_loss, **kwargs)
