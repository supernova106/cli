# Jenkins

## Pipeline Jenkinsfile

- check out git scm

```
stage('Checkout Stash') {
    git branch: '<BRANCH>',
        credentialsId: '93d4b8d1-a0ec-4bfe-8df2-0bc20c5exxxx',
        url: 'ssh://git@REPO'
}
```

- `sh` best practices

```
Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                /* `make check` returns non-zero on test failures,
                * using `true` to allow the Pipeline to continue nonetheless
                */
                sh 'make check || true' 
                junit '**/target/*.xml' 
            }
        }
    }
}
```

- It is worth mentioning that command: 'cat', ttyEnabled: true keeps container running. 

```
podTemplate(label: label, containers: [
  containerTemplate(name: 'gradle', image: 'gradle:4.5.1-jdk9', command: 'cat', ttyEnabled: true),
  containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true),
  containerTemplate(name: 'kubectl', image: 'lachlanevenson/k8s-kubectl:v1.8.8', command: 'cat', ttyEnabled: true),
  containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm:latest', command: 'cat', ttyEnabled: true)
],
volumes: [
  hostPathVolume(mountPath: '/home/gradle/.gradle', hostPath: '/tmp/jenkins/.gradle'),
  hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock')
])
```

- Workspace is also shared between the containers you defined. Pod describe command will give you the exact location 
- Everything within a sh closure is running in the shared workspace. You are specifying different container to run specific commands. Be careful with environment variables. Single quotes vs double quotes and how to access different variables in Groovy
- Also, environment variables like GIT_COMMIT or GIT_BRANCH are not available inside the containers, but you can define them like this:

```
container('gradle') {
  sh """
    echo "GIT_BRANCH=${gitBranch}" >> /etc/environment
    echo "GIT_COMMIT=${gitCommit}" >> /etc/environment
    gradle test
    """
}
```

- In case you need to authenticate docker to DockerHub, create a new username and password credential with dockerhub ID and then use withCredentials pipeline script code to expose username and password as environment variables

```
withCredentials([[$class: 'UsernamePasswordMultiBinding',
  credentialsId: 'dockerhub',
  usernameVariable: 'DOCKER_HUB_USER',
  passwordVariable: 'DOCKER_HUB_PASSWORD']]) {
  sh """
    docker login -u ${DOCKER_HUB_USER} -p ${DOCKER_HUB_PASSWORD}
    docker build -t namespace/my-image:${gitCommit} .
    docker push namespace/my-image:${gitCommit}
    """
}
```