
# mim

well integrated mini machines with rootless podman

## macos

ensure podman machine is initialized as such:

```sh
podman machine init --volume /Users --volume /Volumes
podman machine stop && ulimit -n unlimited && podman machine start
```
