import os
import random
import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sys import platform

"""
dataset.py

Handles download of ADNI dataset into pytorch Dataset and Dataloader. Partitions on the patient level for the train and validation sets.
"""

if platform == "linux" or platform == "linux2":
    TRAIN_FILE_ROOT = "/home/groups/comp3710/ADNI/AD_NC/train"
    TEST_FILE_ROOT = "/home/groups/comp3710/ADNI/AD_NC/test"
else:
    TRAIN_FILE_ROOT = "./AD_NC/train"
    TEST_FILE_ROOT = "./AD_NC/test"

VAL_SIZE = 0.1
TRAIN_SIZE = 0.9


class SiameseDataSet(Dataset):
    """
    Class for loading the ADNI dataset and retrieving the triplet image input
    Reference : https://github.com/maticvl/dataHacker/blob/master/pyTorch/014_siameseNetwork.ipynb
    """

    def __init__(self, imgset: datasets.ImageFolder, transform=None):
        """
        initialise class
        :param imgset: torch.datasets.ImageFolder of ADNI data
        :param transform: Transform to be applied to images to turn them into torch.Tensor instances
        """
        self.imgset = imgset
        self.transform = transform

    def __getitem__(self, index: int):
        """
        overloads function such that item calls return three times, and anchor, a positive class match for the anchor,
        a negative class match for the anchor, and the class label for the anchor
        :param index: integer index to be used to iterate through dataset
        :return: int: class, torch.Tensor: anchor, torch.Tensor: positive anchor match, torch.Tensor: negative anchor match
        """
        anchor_path, anchor_class = self.imgset.samples[index]
        anchor = self.imgset.loader(anchor_path)

        positive = None
        negative = None

        while positive is None or negative is None:
            random_path, random_class = random.choice(self.imgset.imgs)
            if random_path == anchor_path:
                continue
            elif random_class == anchor_class:
                positive = self.imgset.loader(random_path)
            else:
                negative = self.imgset.loader(random_path)

        if self.transform is not None:
            anchor = self.transform(anchor)
            positive = self.transform(positive)
            negative = self.transform(negative)

        return anchor_class, anchor, positive, negative

    def __len__(self):
        # return n_samples
        return len(self.imgset.imgs)


def get_patients(path: str) -> [str]:
    """
    Retrieves a unique list of patients from a folder of patient images
    :param path: path to patient images
    :return: list of unique patient id's found in folder
    """
    uids = []
    dire = os.fsdecode(path)
    for file in os.listdir(dire):
        filename = os.fsdecode(file)
        substrings = filename.split("_", 2)
        if substrings[0] not in uids:
            uids.append(substrings[0])

    # print(f"{path} : {len(uids)}")
    return uids


def remove_patients(imgset: datasets.ImageFolder, index: int, match_set: []) -> datasets.ImageFolder:
    """
    Removes specified pateints in match_set in order to provide a patient level split
    :param imgset: datasets.ImageFolder of loaded ADNI data
    :param index: Class of ADNI photos to search for patients in. 0 = AD, 1 = NC
    :param match_set: list of patients to remove from imgset
    :return: datasets.Imagefolder without images featuring the specified patients match_set
    """
    folder = ""
    if index == 0:
        folder = "AD"
    else:
        folder = "NC"

    for patient in match_set:
        for fname in os.listdir(TRAIN_FILE_ROOT + "/" + folder):
            if patient in fname:
                name = TRAIN_FILE_ROOT + "\\" + folder + "\\" + fname
                if platform == "linux" or platform == "linux2":
                    name = TRAIN_FILE_ROOT + "/" + folder + "/" + fname
                imgset.imgs.remove((name, index))

    return imgset


def get_patient_split() -> (datasets.ImageFolder, datasets.ImageFolder):
    """
    Loads ADNI training set data, retrieves all patients present in the AD and NC classes and performs a patient-level
    split on data to prevent data leakage during training between train and validation sets.
    :return: train and validation ImageFolder's
    """
    files = get_patients(TRAIN_FILE_ROOT + "/AD")
    random.shuffle(files)
    train_ad, validate_ad = np.split(files, [int(len(files) * TRAIN_SIZE)])
    files = get_patients(TRAIN_FILE_ROOT + "/NC")
    random.shuffle(files)
    train_nc, validate_nc = np.split(files, [int(len(files) * TRAIN_SIZE)])

    train_dataset = datasets.ImageFolder(root=TRAIN_FILE_ROOT)
    validation_dataset = datasets.ImageFolder(root=TRAIN_FILE_ROOT)

    train_dataset = remove_patients(train_dataset, 0, validate_ad)
    train_dataset = remove_patients(train_dataset, 1, validate_nc)

    validation_dataset = remove_patients(validation_dataset, 0, train_ad)
    validation_dataset = remove_patients(validation_dataset, 1, train_nc)

    return train_dataset, validation_dataset


def get_test_set() -> DataLoader:
    """
    Loads test set as an isntance of the SiameseDataSet class
    :return:
    """
    return DataLoader(SiameseDataSet(datasets.ImageFolder(root=TEST_FILE_ROOT), compose_transform()),
                      shuffle=True,
                      num_workers=2,
                      batch_size=32)


def compose_transform():
    """
    Compose transform converting image to greyscale, 256x240 sized torch.Tenshor
    :return: series of torchvision.transforms
    """
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((256, 240)),
        transforms.ToTensor()
    ])


def load() -> (SiameseDataSet, SiameseDataSet):
    """
    Loads patient-level split training and validation image sets into an instance of SiameseDataSet
    :return: training and validation SiaemseDataSet's
    """
    trainer, val = get_patient_split()
    transform = compose_transform()

    trainSet = SiameseDataSet(trainer, transform)
    valSet = SiameseDataSet(val, transform)

    trainDataLoader = DataLoader(trainSet, shuffle=True, num_workers=2, batch_size=32)
    valDataLoader = DataLoader(valSet, shuffle=True, num_workers=2, batch_size=32)

    return trainDataLoader, valDataLoader


if __name__ == "__main__":
    pass
