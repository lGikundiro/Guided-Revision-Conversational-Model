"""Model training, evaluation and saving for UrbanSound8K mel-spectrograms"""
import os
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib


def build_model(input_shape, num_classes):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Reshape((*input_shape, 1)),
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPool2D((2,2)),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPool2D((2,2)),
        layers.Conv2D(128, (3,3), activation='relu'),
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def train(data_dir, model_output, epochs=10, batch_size=32, test_size=0.2):
    X = np.load(os.path.join(data_dir, 'X.npy'))
    y = np.load(os.path.join(data_dir, 'y.npy'))
    classes = list(np.loadtxt(os.path.join(data_dir, 'classes.csv'), dtype=str, delimiter='\n'))
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)

    input_shape = X_train.shape[1:]
    model = build_model(input_shape, num_classes=len(classes))
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)
    # evaluate
    preds = np.argmax(model.predict(X_val), axis=1)
    print(classification_report(y_val, preds))
    print('Confusion matrix:')
    print(confusion_matrix(y_val, preds))
    # save
    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    model.save(model_output)
    joblib.dump(classes, os.path.join(os.path.dirname(model_output), 'classes.joblib'))
    print('Saved model to', model_output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--model_output', required=True)
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--epochs', type=int, default=10)
    args = parser.parse_args()
    if args.train:
        train(args.data, args.model_output, epochs=args.epochs)


if __name__ == '__main__':
    main()
