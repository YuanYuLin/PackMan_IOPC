- Folder structure:

1. Package name
 * <package_name>:				args['pkg_name']
2. Folder for source 
 * packages/<package_name>:			args['pkg_path']
3. Folder for development build
 * output/<package_name>:			args['output_path']
4. Base rootfs for development and binary objects; 
   The path is overrided by "debootstrap" package.
 * output/<package_arch>:			iopc.getOutputRootDir()
5. Folder for binary files package 
 * output/<package_arch>/pakcages_dir:		iopc.getBinPkgPath()
6. Folder for output target files.
 * output/<package_arch>/rootfs:		iopc.getTargetRootfs()
7. Folder for developemnt 
 * output/<package_arch>/sdkstage:		iopc.getSdkPath()
 * output/<package_arch>/sdkstage/usr/include:	iopc.getSdkInclude()
 * output/<package_arch>/sdkstage/usr/lib:	iopc.getSdkLib()
 * output/<package_arch>/sdkstage/pkgconfig:	iopc.getSdkPkgConfig()

- Image layout
GPT: reserved 1048576 bytes for partitions
MBR: reserved 512     bytes for partitions

 ------------------ 0
 |  MBR
 ------------------ 512
 |
 |  GPT
 |
 ------------------1048576 - 1M
 |  IOPC HEADER            - 64K
 ------------------1114112
 |  IOPC DAO
 ------------------N
 |  Partitions
 |
 |
