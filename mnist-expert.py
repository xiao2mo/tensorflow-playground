from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

import tensorflow as tf

sess = tf.InteractiveSession()

#input format: flattened 28x28 pixel image
x = tf.placeholder(tf.float32, [None, 784])
#output format: one-hot 10dim vector indicating which digit the image corresponds to
y_ = tf.placeholder(tf.float32, [None, 10])

#weights for model
W = tf.Variable(tf.zeros([784,10]))
#biases for model
b = tf.Variable(tf.zeros([10]))

#initialize variables within session
sess.run(tf.global_variables_initializer())

# regression model: input image x * weight W + bias b
y = tf.matmul(x,W) + b

#loss function:
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))

#define one training iteration:
train_step = tf.train.GradientDescentOptimizer(.5).minimize(cross_entropy)

#train 1000 iterations
for i in range(1000):
    batch = mnist.train.next_batch(100)
    train_step.run(feed_dict={x: batch[0], y_: batch[1]})

#define correct answer: is_correct? is True iff arg 1 in y (array of correct answers)
#is equal to index 1 in y_ (array of outputs)
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

#Turn T/F to floats 1/0 and evaluate mean
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#print results
print(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

#the following two functions will define a weight variable and a bias variable for each neuron
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape) #initialized positive to prevent dead neurons
    return tf.Variable(initial)

#defines convolution for easy typing
def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
#defines max pooling for easy typing
def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')
#first convolutional layer
W_conv1 = weight_variable([5,5,1,32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1,28,28,1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

#max pooling
h_pool1 = max_pool_2x2(h_conv1)

#second convolutional layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

#dropout: overfitting preventer
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

#softmax output layer
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())
for i in range(20000):
  batch = mnist.train.next_batch(50)
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch[0], y_: batch[1], keep_prob: 1.0})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))