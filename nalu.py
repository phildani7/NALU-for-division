import numpy as np
import tensorflow as tf

def nalu(inputs,out_units,sigma):
	
	in_features = inputs.shape[1]
		
	W_hat = tf.get_variable(name = "W_hat", initializer=tf.initializers.random_uniform(minval=-2, maxval=2),shape=[in_features, out_units],  trainable=True, dtype = tf.float64)
	M_hat = tf.get_variable(name = "M_hat", initializer=tf.initializers.random_uniform(minval=-2, maxval=2), shape=[in_features, out_units], trainable=True, dtype = tf.float64)
	
	G = tf.get_variable(name = "G", initializer=tf.initializers.random_uniform(minval=-2, maxval=2),shape=[in_features, out_units],  trainable=True, dtype = tf.float64)

	W = tf.tanh(W_hat) * tf.sigmoid(M_hat)
	
	a = tf.matmul(inputs,W)
	m = tf.exp(tf.matmul(tf.log(tf.abs(inputs) + sigma), W))

	g = tf.sigmoid(tf.matmul(inputs,G))

	out = g * a + (1-g) * m

	return out, W

#############   NALU DEFINED ###########

def generate_dataset(size = 10000, operation = 'sum', task = 'in'):
	if task == 'in':
		factor = 1000
	else:
		factor = 5000

	#power = np.random.choice(a = [0,1], p = [0.5,0.5])
	
	X = factor * np.random.ranf(size = (size, 2))

	if operation == 'prod':
		Y = np.prod(X, axis=1, keepdims = True)

	else:
		Y = np.sum(X, axis=1, keepdims = True)

	
	return X,Y

#########################

if __name__ == '__main__':
	EPOCHS = 100000
	LEARNING_RATE = 1e-3
	SIGMA = 1e-7


	X_data, Y_data = generate_dataset(operation = 'prod')
	X_test, Y_test = generate_dataset(size = 1000, operation = 'prod', task = 'ex')
	
	X = tf.placeholder(tf.float64, shape = [None,2])
	Y = tf.placeholder(tf.float64, shape = [None,1])

	Y_pred, W = nalu(X,1,SIGMA)

	loss = tf.losses.mean_squared_error(labels = Y, predictions = Y_pred)
	optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss)

	with tf.Session() as sess:
		cost_history = []
		sess.run(tf.global_variables_initializer())

		print('Pre training MSE: ',sess.run(loss, feed_dict = {X : X_data, Y : Y_data}))
		print()

		for i in range(EPOCHS):
			_,cost = sess.run([optimizer, loss], feed_dict = {X : X_data, Y : Y_data})
			print('epoch: {}, MSE: {}'.format(i,cost))
			cost_history.append(cost)

		print()
		print(W.eval())
		print()


		print("post training MSE", sess.run(loss, feed_dict = {X:X_test, Y:Y_test}))

		print("Actual Sum: ",Y_test[0:20])
		print()
		print("predicted sum: ", sess.run(Y_pred[0:20], feed_dict = {X:X_test, Y: Y_test}))

		print()
		print()
		print(X_data[0:10])
		print()
		print(X_test[0:10])
 		

		
			
		

		
		





