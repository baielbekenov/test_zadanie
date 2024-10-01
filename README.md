Запуск раннера

docker run -d --name gitlab-runner --restart always \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    -v /var/run/docker.sock:/var/run/docker.sock \
    gitlab/gitlab-runner:alpine

Регистрация раннера

docker run --rm -t \
-v /srv/gitlab-runner/config:/etc/gitlab-runner \
gitlab/gitlab-runner:alpine register