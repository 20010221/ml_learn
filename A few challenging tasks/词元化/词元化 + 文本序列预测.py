import collections
import pandas as pd
import tensorflow as tf
import keras

from tensorflow.keras.layers import TextVectorization

data = pd.read_csv('corpus.txt',header=None,names=['text'])
texts = data['text'].values
vec = TextVectorization(max_tokens=2000,output_mode='int',output_sequence_length=3,split="whitespace")
vec.adapt(texts)
vocabulary = vec.get_vocabulary()
vectorized_texts = vec(texts)


def split_input_target(sequence):
    input_seq = sequence[:-1]
    target_seq = sequence[1:]
    return input_seq, target_seq

dataset = tf.data.Dataset.from_tensor_slices(vectorized_texts)
sequence_dataset =dataset.map(split_input_target)

total_samples = len(vectorized_texts)
train_size = int(0.8 * total_samples)
train_ds = sequence_dataset.take(train_size).shuffle(1000).batch(32)
val_ds = sequence_dataset.skip(train_size).batch(32)

hidden_dim = 64
inputs = keras.Input(shape=(2,), dtype="int32")
x = tf.keras.layers.Embedding(input_dim=2000, output_dim=hidden_dim, mask_zero=True)(inputs)
x = tf.keras.layers.LSTM(hidden_dim, return_sequences=True)(x)  # 返回每个时间步输出
outputs = tf.keras.layers.Dense(2000, activation="softmax")(x)  # 输出每个时间步的词概率
model = keras.Model(inputs, outputs, name="lstm_with_embedding")
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",  # 序列预测用这个损失
    metrics=["accuracy"]
)


early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    restore_best_weights=True,
    patience=2,)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    callbacks=[early_stopping]
)
model.summary()


def generate_text(model, vectorizer, start_text, max_length=50,end_token=None):
    input_sequence = vectorizer([start_text])
    input_sequence = input_sequence[:, -2:]
    generated_text = start_text
    start_word_count = len(start_text.split())
    for _ in range(max_length - start_word_count):

        prediction = model.predict(input_sequence, verbose=0)
        predicted_index = tf.argmax(prediction[0, -1, :]).numpy()
        vocab = vectorizer.get_vocabulary()
        if predicted_index < len(vocab):
            predicted_word = vocab[predicted_index]
        else:
            predicted_word = "[UNK]"
        if end_token and predicted_word == end_token:
            break
        generated_text += " " + predicted_word
        next_token_tensor = tf.constant([[predicted_index]], dtype=tf.int64)
        input_sequence = tf.concat([input_sequence[:,1:],next_token_tensor], axis=1)
    return generated_text

start_text = '我喜欢深度'
generated = generate_text(model, vec, start_text, max_length=6)
print( generated)
