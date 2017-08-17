#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import json


if __name__ == '__main__':

	x = np.arange(100)
	y = x*x
	z = x*x + 10*x

	with open("style.json") as json_file:
	    s = json.load(json_file)


	plt.rcParams.update(s)

	plt.plot(x,y,label='Y=x*x');
	plt.plot(x,z,label='Y=x*x+10*x');
	plt.title('Nice JSON example');
	plt.legend();
	plt.plot();
	plt.savefig('json_example.png')