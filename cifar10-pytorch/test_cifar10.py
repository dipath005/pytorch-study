# -*- coding: utf-8 -*-

import os, sys, pdb
import argparse

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F

from models import alexnet, vgg, resnet, densenet
from loader import test_loader, cifar10_classes

def set_args():
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size',      type=int,   default=32)
    parser.add_argument('--seed',            type=int,   default=3)
    parser.add_argument('--device_id',       type=int,   default=0)
    # model directory and name
    parser.add_argument('--model-dir',       type=str,   default="../models/CIFAR10/AlexNet")
    parser.add_argument('--model-name',      type=str,   default="cifar10-300.pth")

    args = parser.parse_args()
    return args

def test(data_loader, model, args):
    # Load model
    weights_path = os.path.join(args.model_dir, args.model_name)
    model.load_state_dict(torch.load(weights_path))

    model.eval()
    test_loss, correct, total = 0.0, 0, 0
    criterion = nn.CrossEntropyLoss()
    for inputs, targets in data_loader:
        if args.cuda:
            inputs, targets = inputs.cuda(args.device_id), targets.cuda(args.device_id)
        inputs, targets = Variable(inputs), Variable(targets)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        test_loss += loss.item()

        _, preds = outputs.max(1)
        total += targets.size(0)
        correct += preds.eq(targets).sum().item()

    test_loss /= len(data_loader.dataset)
    acc = 100.*correct/total
    print("\n Test set: Average loss: {:.4f}, Accuracy: {}/{} {:.4f}\n".format(
        test_loss, correct, total, correct*1.0 / total))

if __name__ == '__main__':
    args = set_args()
    args.cuda = torch.cuda.is_available()
    torch.manual_seed(args.seed)
    model = alexnet.AlexNet(num_classes=len(cifar10_classes))
    # model = vgg.VGG('VGG16', len(cifar10_classes))
    # model = vgg.VGG('VGG19', len(cifar10_classes))
    # model = resnet.ResNet50(num_classes=len(cifar10_classes))
    # model = resnet.ResNet101(num_classes=len(cifar10_classes))
    # model = densenet.DenseNet121(num_classes=len(cifar10_classes))
    # model = densenet.DenseNet201(num_classes=len(cifar10_classes))

    if args.cuda:
        torch.cuda.manual_seed(args.seed)
        model.cuda(args.device_id)
        import torch.backends.cudnn as cudnn
        cudnn.benchmark = True

    # dataloader
    data_loader = test_loader(args)
    # start testing
    test(data_loader, model, args)
