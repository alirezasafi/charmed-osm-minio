# charmed-osm-minio

## Create And Onboard minio service using osm.

> To create osm vnf and ns package, use the following commands which will
> generate a vnf package structure named minio_vnf and ns package structure
> named minio_ns

```bash
# in the rep root dir execute the following commands.
osm nfpkg-create minio_vnf/
osm nspkg-create minio_ns/
```

> Onboarded package can be verified with the following commands.

```bash
osm nfpkg-list # or use osm vnfd-list
osm nspkg-list # or use osm nsd-list
```

## Create dummy VIM account

> Create a dummy vim that can be used when the k8scluster being added to osm.

```bash
osm vim-create --namd <vim-name> --account_type dummy
```
> if there is a proper VIM like openstack, use the following command.

```bash
osm vim-create --name <vim-name> --user <username> --password <password> \
    --auth_url <openstack-url> --tenet <tenant-name> --account_type openstack
```
* `vim-name` is the name of the vim being created.
* `username` and `password` are the credentials of openstack.
* `tenant-name` is the tenant to be assosiated to the user in the openstack.
* `openstack-url` is the url of openstack which will be used as VIM.

## Add k8s-cluster
> K8scluster used to attach a cluster with OSM which will be used for knf deployment.


```bash
osm k8scluster-add --creds <k8s-config-file>  --version v1 --vim <vim-name> --description 'K8s Cluster for KNFs' --k8s-nets '{"net1": "vim-net"}' <cluster-name>
```

* `k8s-config-file` is the configuration file of kubernetes cluster.

## Instantiating of the minio network service.

> To instantiating the minio network service use the following command.
```bash
osm ns-create --ns_name <ns-name> --nsd_name minio_ns --vim_account <vim-name>
```

> To verifying the instantiating process use the following commands.

```bash
# with the osm client
osm ns-list
# for detail information
osm ns-show
# use kubectl command.
kubectl -n minio-kdu-*** get pods
```

### Execute day2 operations

> To execute addurl action that add specific dommain to squid allowed
> domains, use the following command.

```bash
osm ns-action <ns-name> --vnf_name 1 --kdu_name minio-kdu --action_name addurl \
    --params '{url: "<domain-name>"}'
```

> To execute deleteurl action that deleete added domain from
> squid domains, use the following command.

```bash
osm ns-action <ns-name> --vnf_name 1 --kdu_name minio-kdu --action_name deleteurl \
    --params '{url: "<domain-name>"}'
```

> To execute send file action that send some sample file from source
> to destination service use the following command
```bash
osm ns-action <ns-name> --vnf_name 1 --kdu_name minio-kdu --action_name sendfile \
     --params '{endpoint: "http://minio-dst:9000", access-key: "minio", secret-key: "MinioP@ss", target-bucket: "samples", source-filename: "test.txt"}'
```
