sudo docker build worker --tag worker
sudo docker build master --tag master
# sudo docker-compose up
sudo docker stack init
sudo docker stack deploy --compose-file docker-stack.yml vote
