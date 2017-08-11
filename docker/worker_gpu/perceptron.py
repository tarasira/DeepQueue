import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist=input_data.read_data_sets('MNIST_data',one_hot=True)

sess=tf.InteractiveSession()
x  =tf.placeholder(tf.float32,shape=[None,784]) #28*28
y_ =tf.placeholder(tf.float32,shape=[None,10])
W  =tf.Variable(tf.zeros([784,10]),tf.float32)
b  =tf.Variable(tf.zeros([10]),tf.float32)

#sess.run( tf.initialize_all_variables() )
sess.run( tf.global_variables_initializer() )

y=tf.nn.softmax( tf.matmul(x,W)+b )
cross_entropy=tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y),reduction_indices=[1]))
train_step=tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

for i in range(1000):
    batch=mnist.train.next_batch(50)
    train_step.run(feed_dict={x:batch[0], y_:batch[1]})

correct_prediction=tf.equal(tf.argmax(y,1),tf.arg_max(y_,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
acc=accuracy.eval(feed_dict={x:mnist.test.images, y_:mnist.test.labels})*100
print "Accuracy of the ANN is %s"%acc

sess.close()