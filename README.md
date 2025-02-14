# Siamese Network

## Aim
This project was developed as an assessment item for course COMP3710 at the University of Queensland. It comprises a Siamese neural net for the binary classification of alzheimers disease.

We create pattern recognition and image processing library for Tensorflow (TF), PyTorch or JAX. This library is created and maintained by The University of Queensland [COMP3710](https://my.uq.edu.au/programs-courses/course.html?course_code=comp3710) students.

## Algorithm Logic
The model comprises a triple siamese convolutional neural network and a binary classifier. The model is trained to 
classify 2D images slices of brain scans as Alzheimer's disease (AD) and normal cognitive (NC)

The siamese network consists of three convolutional neural networks, each with shared weights and structure. Of the CNN's, one is an anchor, one is a positive and one is a negative.
They take in a triplet of images, one of which is the anchor, one which is a positive match and one which is a negative match. For example, 
for Alzheimer's if the anchor is AD, then the positive image is also AD, and the negative is NC. 

During training, a contrastive loss function takes in the features of the network output and calculates loss to maximise 
the loss between the anchor and the negative, and minimise the loss between the anchor and the positive.

Once training is completed on the siamese network, we can use the siamese embeddings on the image input to another convolutional neural network,
this a binary classifier and outputs a answer for which class (AD or NC) the given image is.

![Siamese triplet diagram](https://github.com/tweeeb/siamese-nn/blob/topic-recognition/recognition/assets/triplet_siamese.jpg?raw=true)

## Data Pre-Processing
### Transforms
Data is pre-proccessed to be of size 256x240 and converted to greyscale (so the siamese model takes in 1 channel instead of 3) as these are the only features that matter. No other transformations are done as the input image format is relatively constant.

### Data partitions
Data is partitioned by patient to prevent data leakage. This is to prevent the model from seeing data from the same patient in the validation set or in the test set while being trained.

## Project Structure
## Run
To train models, run train.py

To see accuracy of models, run predict.py

Please note, the data is retrieved via the rangpur location if on a linux system, and is retrieved via the file structure nominated in the readme on a windows system. Adjustments can be made to the filepath at the top of the dataset.py file if this is not the configuration preferred.

## Dependencies

- matplotlib 3.7.2
- numpy 1.24.3
- torch 2.1.0

## File Structure

This project uses the ADNI dataset for Alzheimer's disease. Please format the data under the directory AD_NC in 
this repository accordingly.

```
recognition
├── modules.py
├── dataset.py
├── predict.py
├── train.py
├── utils.py
├── .gitignore
├── slurm.sh
├── assets
|   └── triplet_siamese.jpg
└── AD_NC
    ├── test
    |    ├── AD
    |    |   └── 388206_78.jpeg
    |    |              .
    |    |              .
    |    |              .
    |    └── NC
    |    |   └── 1182968_88.jpeg
    |    |              .
    |    |              .
    |    |              .
    └── train
         ├── AD
         |   └── 218391_78.jpeg
         |              .
         |              .
         |              .
         └── NC
             └── 808819_88.jpeg
                        .
                        .
                        .
```