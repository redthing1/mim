
# mim

well integrated mini machines with rootless podman.
a minimalist implementation.

## setup

### linux

should be all good to go

### macos

ensure podman machine is initialized as such:

```sh
podman machine init --volume /Users --volume /Volumes
podman machine stop && ulimit -n unlimited && podman machine start
```

## usage

### build a mimchine image

```sh
mim build -f ./demo/mim_fed.docker -n mim_fed
```

### create a mimchine

```sh
mim create -n mim_fed -H ~/Downloads
```

### open a shell in a mimchine

```sh
mim shell -c mim_fed
```

### destroy a mimchine

```sh
mim destroy -c mim_fed -f
```
