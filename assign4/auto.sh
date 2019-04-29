while true
do 
	python2 chat_client.py | tail -n 1 >> keys
	echo "key loaded..."
done