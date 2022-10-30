# anonymous anonymous 2020
# coral_pytorch
# Author: anonymous anonymous <sebastiananonymous.com>
#
# License: MIT

import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import pandas as pd
import os


def label_to_levels(label, num_classes, dtype=torch.float32):
    """Converts integer class label to extended binary label vector

    Parameters
    ----------
    label : int
        Class label to be converted into a extended
        binary vector. Should be smaller than num_classes-1.

    num_classes : int
        The number of class clabels in the dataset. Assumes
        class labels start at 0. Determines the size of the
        output vector.

    dtype : torch data type (default=torch.float32)
        Data type of the torch output vector for the
        extended binary labels.

    Returns
    ----------
    levels : torch.tensor, shape=(num_classes-1,)
        Extended binary label vector. Type is determined
        by the `dtype` parameter.

    Examples
    ----------
    >>> label_to_levels(0, num_classes=5)
    tensor([0., 0., 0., 0.])
    >>> label_to_levels(1, num_classes=5)
    tensor([1., 0., 0., 0.])
    >>> label_to_levels(3, num_classes=5)
    tensor([1., 1., 1., 0.])
    >>> label_to_levels(4, num_classes=5)
    tensor([1., 1., 1., 1.])
    """
    if not label <= num_classes-1:
        raise ValueError('Class label must be smaller or '
                         'equal to %d (num_classes-1). Got %d.'
                         % (num_classes-1, label))
    if isinstance(label, torch.Tensor):
        int_label = label.item()
    else:
        int_label = label

    levels = [1]*int_label + [0]*(num_classes - 1 - int_label)
    levels = torch.tensor(levels, dtype=dtype)
    return levels


def levels_from_labelbatch(labels, num_classes, dtype=torch.float32):
    """
    Converts a list of integer class label to extended binary label vectors

    Parameters
    ----------
    labels : list or 1D orch.tensor, shape=(num_labels,)
        A list or 1D torch.tensor with integer class labels
        to be converted into extended binary label vectors.

    num_classes : int
        The number of class clabels in the dataset. Assumes
        class labels start at 0. Determines the size of the
        output vector.

    dtype : torch data type (default=torch.float32)
        Data type of the torch output vector for the
        extended binary labels.

    Returns
    ----------
    levels : torch.tensor, shape=(num_labels, num_classes-1)

    Examples
    ----------
    >>> levels_from_labelbatch(labels=[2, 1, 4], num_classes=5)
    tensor([[1., 1., 0., 0.],
            [1., 0., 0., 0.],
            [1., 1., 1., 1.]])
    """
    levels = []
    for label in labels:
        levels_from_label = label_to_levels(
            label=label, num_classes=num_classes, dtype=dtype)
        levels.append(levels_from_label)

    levels = torch.stack(levels)
    return levels


def proba_to_label(probas):
    """
    Converts predicted probabilities from extended binary format
    to integer class labels

    Parameters
    ----------
    probas : torch.tensor, shape(n_examples, n_labels)
        Torch tensor consisting of probabilities returned by CORAL model.

    Examples
    ----------
    >>> # 3 training examples, 6 classes
    >>> probas = torch.tensor([[0.934, 0.861, 0.323, 0.492, 0.295],
    ...                        [0.496, 0.485, 0.267, 0.124, 0.058],
    ...                        [0.985, 0.967, 0.920, 0.819, 0.506]])
    >>> proba_to_label(probas)
    tensor([2, 0, 5])
    """
    predict_levels = probas > 0.5
    predicted_labels = torch.sum(predict_levels, dim=1)
    return predicted_labels

def proba_to_label_wenzhi(probas):
    comp_1 = torch.cat((torch.ones(probas.shape), torch.cumprod(probas, dim=1)))
    comp_2 = torch.cat((1-probas, torch.ones(probas.shape)))
    probas_y = torch.mul(comp_1, comp_2)
    labels = torch.argmax(probas_y,dim=1)
    return labels

def mnist_train_transform():
    return transforms.Compose([transforms.ToTensor()])


def mnist_validation_transform():
    return transforms.Compose([transforms.ToTensor()])

##################################################################################


class Morph2Dataset(Dataset):
    """Custom Dataset for loading MORPH face images"""

    def __init__(self,
                 csv_path, img_dir, transform=None):

        df = pd.read_csv(csv_path, index_col=0)
        self.img_dir = img_dir
        self.csv_path = csv_path
        self.img_names = df.index.values
        self.y = df['age'].values
        self.transform = transform

    def __getitem__(self, index):
        img = Image.open(os.path.join(self.img_dir,
                                      self.img_names[index]))

        if self.transform is not None:
            img = self.transform(img)

        label = self.y[index]

        return img, label

    def __len__(self):
        return self.y.shape[0]


def morph2_train_transform():
    return transforms.Compose([transforms.CenterCrop((140, 140)),
                               transforms.Resize((128, 128)),
                               transforms.RandomCrop((120, 120)),
                               transforms.ToTensor()])


def morph2_validation_transform():
    return transforms.Compose([transforms.CenterCrop((140, 140)),
                               transforms.Resize((128, 128)),
                               transforms.CenterCrop((120, 120)),
                               transforms.ToTensor()])

class AesDataset(Dataset):
    """Custom Dataset for loading MORPH face images"""

    def __init__(self,
                 csv_path, img_dir, transform=None):

        df = pd.read_csv(csv_path, index_col=0)
        self.img_dir = img_dir
        self.csv_path = csv_path
        self.img_names = df.index.values
        self.y = df['beauty_scores'].values
        self.transform = transform

    def __getitem__(self, index):
        img = Image.open(os.path.join(self.img_dir,
                                      self.img_names[index]))

        if self.transform is not None:
            img = self.transform(img)
            if img.shape[0] == 1:
                img = torch.cat(list(torch.split(img, 1, dim=0))*3)
        label = self.y[index]

        return img, label

    def __len__(self):
        return self.y.shape[0]


def aes_train_transform():
    return transforms.Compose([transforms.CenterCrop((140, 140)),
                               transforms.Resize((128, 128)),
                               transforms.RandomCrop((120, 120)),
                               transforms.ToTensor()])


def aes_validation_transform():
    return transforms.Compose([transforms.CenterCrop((140, 140)),
                               transforms.Resize((128, 128)),
                               transforms.CenterCrop((120, 120)),
                               transforms.ToTensor()])

# class AfadDataset(Dataset):
#     """Custom Dataset for loading MORPH face images"""

#     def __init__(self,
#                  csv_path, img_dir, transform=None):

#         df = pd.read_csv(csv_path, index_col=0)
#         self.img_dir = img_dir
#         self.csv_path = csv_path
#         self.img_names = df.index.values
#         self.y = df['age'].values
#         self.transform = transform

#     def __getitem__(self, index):
#         img = Image.open(os.path.join(self.img_dir,
#                                       self.img_names[index]))

#         if self.transform is not None:
#             img = self.transform(img)
#             if img.shape[0] == 1:
#                 img = torch.cat(list(torch.split(img, 1, dim=0))*3)
#         label = self.y[index]

#         return img, label

#     def __len__(self):
#         return self.y.shape[0]

class AfadDatasetAge(Dataset):
    """Custom Dataset for loading AFAD face images"""

    def __init__(self, csv_path, img_dir, transform=None):

        df = pd.read_csv(csv_path, index_col=0)
        self.img_dir = img_dir
        self.csv_path = csv_path
        self.img_paths = df['path']
        self.y = df['age'].values
        self.transform = transform

    def __getitem__(self, index):
        img = Image.open(os.path.join(self.img_dir,
                                      self.img_paths[index]))

        if self.transform is not None:
            img = self.transform(img)

        label = self.y[index]

        return img, label

    def __len__(self):
        return self.y.shape[0]


def afad_train_transform():
    return transforms.Compose([transforms.CenterCrop((140, 140)),
                               transforms.Resize((128, 128)),
                               transforms.RandomCrop((120, 120)),
                               transforms.ToTensor()])


def afad_validation_transform():
    return transforms.Compose([transforms.CenterCrop((140, 140)),
                               transforms.Resize((128, 128)),
                               transforms.CenterCrop((120, 120)),
                               transforms.ToTensor()])

def get_labels_from_loader(data_loader):
    # lst = []
    # for batch_idx, (features, targets) in enumerate(data_loader):
    #     lst.append(targets)
    # return torch.cat(lst)
    lst = []
    for batch_idx, batch_data in enumerate(data_loader):
        features, text_length = batch_data.TEXT_COLUMN_NAME
        labels = batch_data.LABEL_COLUMN_NAME
        lst.append(labels)
    return torch.cat(lst)

