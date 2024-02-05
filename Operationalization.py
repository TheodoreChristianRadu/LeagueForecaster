import json
import tensorflow as tf
from tensorflow import keras
from keras import models
from collections import defaultdict

with open('structure.json', 'r') as file:
    structure = json.load(file)

with open('model.json', 'r') as file:
    model = models.model_from_json(file.read())
model.load_weights("model.keras")
mean = tf.io.parse_tensor(tf.io.read_file("mean.tfrecord"), out_type=tf.float32)
deviation = tf.io.parse_tensor(tf.io.read_file("deviation.tfrecord"), out_type=tf.float32)

def profile(history):
    counts = defaultdict(int)
    for j in range(len(history)):
        for k in range(10):
            icon = history[j]["participants"][k]["profileIcon"]
            counts[icon] += 1
    return max(counts, key=counts.get)

def predict(data):
    history = []
    icon = profile(data)
    for i in range(len(data)): # Game
        game = []
        players = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for k in range(5, 10):
            if data[i]["participants"][k]["profileIcon"] == icon:
                players = [5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
        for k in players: # Participant
            for key, value in structure.items():
                if len(value) == 0:
                    game.append(data[i]["participants"][k][key])
                else:
                    game.append(value.index(data[i]["participants"][k][key]))
        history.append(game)

    dataset = tf.ragged.constant([history], ragged_rank=1, dtype=tf.float32)
    dataset = (dataset - mean) / deviation

    result = model(dataset)[0][-1]
    result = mean + result * deviation
    return result[0][0]
