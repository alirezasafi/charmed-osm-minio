# charmed-osm-minio

### Create VIM account on OSM
- `osm vim-create --name hackfest-dummy --accout_type dummy`

### Add k8s-cluster
- `osm k8scluster-add --creds $K8S_CONFIG_PATH  --version v1 --vim hackfest-dummy --description 'K8s Cluster for KNFs' --k8s-nets '{"net1": "vim-net"}' cluster`

### Build ackages ith OSM client
- `osm nfpkg-create minio_vnf`
- `osm nspkg-create minio_ns`

### create network service instance
- `osm ns-create --ns_name minio_ns --nsd_name minio_nsd --vim_account hackfest-dummy`

### Execute day2 actions
- `osm ns-action minio_ns --vnf_name 1 --kdu_name minio-kdu --action_name sendfile  --params '{endpoint: "http://minio-dst:9000", access-key: "minio", secret-key: "MinioP@ss", target-bucket: "samples", source-filename: "test.txt"}'`
