# Changelog

## 0.1.0 (2023-07-20)


### ⚠ BREAKING CHANGES

* make all models mutable
* discord models are no longer attr classes
* **Flag:** definition of flag members
* how models are defined

### Features

* add application command models ([1fadde9](https://github.com/discatpy-dev/library/commit/1fadde9a1c2269bc6519d167ba77c16c22d76131))
* add Bot.user ([bc8a502](https://github.com/discatpy-dev/library/commit/bc8a5028dbc52cb2c5e0a05b4c6c3ac74974edbd))
* add embed data class ([f59a007](https://github.com/discatpy-dev/library/commit/f59a0074f25821514d93d2896b0df689a244da58))
* add intents flag ([4934544](https://github.com/discatpy-dev/library/commit/4934544d46969d410c01c7b21d8223b3dcbf5245))
* add PermissionOverwrite.set ([0c211a2](https://github.com/discatpy-dev/library/commit/0c211a20108ae987bd57ed857566b8ec9b58e830))
* **attr_exts:** correctly typed attr.fields alternative ([7ba0f8f](https://github.com/discatpy-dev/library/commit/7ba0f8f6f1e803c8e3ccfcb1c880a41f26ea4821))
* **Bot:** add heartbeat_timeout parameter ([86378bf](https://github.com/discatpy-dev/library/commit/86378bff5151ed4f04b9b9f282e3c2d939436a65))
* **Flag:** remove _has_value ([40890f1](https://github.com/discatpy-dev/library/commit/40890f107720347121cf22e5ed61cf89bb63b59d))
* **flags:** add ACTIVE_DEVELOPER flag ([#17](https://github.com/discatpy-dev/library/issues/17)) ([650ad4e](https://github.com/discatpy-dev/library/commit/650ad4e6706b873552eafed0acc8954382430065))
* **Flags:** add more dunders for compatibility ([ce0a35e](https://github.com/discatpy-dev/library/commit/ce0a35ee97c2bc0e833c748cf9e3798c82a0a1c6))
* **frozen_for_public:** check for custom setattr with all bases ([acb3040](https://github.com/discatpy-dev/library/commit/acb3040eb7b1debfb102f976d9f39ee4cc417495))
* initial commit ([c7f34ad](https://github.com/discatpy-dev/library/commit/c7f34ad4d9d8ef615897438dab7e47860624972e))
* **PermissionOverwrite:** allow params to be netural ([#22](https://github.com/discatpy-dev/library/issues/22)) ([28d07c1](https://github.com/discatpy-dev/library/commit/28d07c1752fed0c154924e6f41faf84992b3739b))
* permissions & permissionoverwrite ([58f84c0](https://github.com/discatpy-dev/library/commit/58f84c0531661714475d0aabeaaf5125d264bdc6))
* preparation for channel models ([e4c4bf5](https://github.com/discatpy-dev/library/commit/e4c4bf5778b1047b474bd5d26db0e07aa19a88e9))
* **utils.typing:** remove evalulate_annotations ([695cbcf](https://github.com/discatpy-dev/library/commit/695cbcf42d44835b2cf53b1759c9bcc4616691e6))


### Bug Fixes

* 3.9 does not support unions in isinstance ([307bdbe](https://github.com/discatpy-dev/library/commit/307bdbefcef162b854ddaba87f4f45efcbb144f5))
* **Asset:** formatted_url doesn't return the fully formatted asset url ([f0f8010](https://github.com/discatpy-dev/library/commit/f0f8010df41d462c0505ea81f28391c2fd43832d))
* **attr_exts:** frozen_for_public did not patch deleting attributes ([215427a](https://github.com/discatpy-dev/library/commit/215427a823f6952159af81a62ab6648077c7c38d))
* **attr_exts:** pyright errors ([ea142be](https://github.com/discatpy-dev/library/commit/ea142bef34c284171aee7a7c37b1871f6169475c))
* attrs.field has default param for a reason ([55de925](https://github.com/discatpy-dev/library/commit/55de9258ee55c94fc0fe6d5830d0d8d9583450b2))
* breaking changes w/ newer version of discatcore ([17a7fc7](https://github.com/discatpy-dev/library/commit/17a7fc75ae3bc6a992d95179538fffd8deb702d4))
* **Embed:** converters couldn't handle None parameters ([21c9274](https://github.com/discatpy-dev/library/commit/21c92744938a740c99fefb668d6563f9f98655b3))
* **Embed:** ToDictMixin doesn't convert parameters that need conversion ([123d825](https://github.com/discatpy-dev/library/commit/123d825ca387c770285683b8bca8c63488ceebd8))
* event protos required self parameter ([12d07e0](https://github.com/discatpy-dev/library/commit/12d07e062b307012d1fc300242bc1a22007d0476))
* **frozen_for_public:** every generated dunder was named __setattr__ ([489bf7c](https://github.com/discatpy-dev/library/commit/489bf7c1379d4a381af7b9710c372af329f3ce5a))
* **Message:** typo with dictionary key ([2f10478](https://github.com/discatpy-dev/library/commit/2f10478408022ae70eb4d5fb25e39ff521ea5d77))
* old pyright ignore comment ([9db2f88](https://github.com/discatpy-dev/library/commit/9db2f88a3272bf2782b9604961e53456e38554d3))
* PermissionOverwrite did not properly handle allows and denies ([65287d2](https://github.com/discatpy-dev/library/commit/65287d2571f42784862373fa91c33d00feafe7f2))
* type ignore comment in the wrong place ([a7f58c8](https://github.com/discatpy-dev/library/commit/a7f58c8bb611c3e53302e6ca0e8962d1e4d703ec))
* **User:** default user avatar wasn't set if no custom avatar ([208455f](https://github.com/discatpy-dev/library/commit/208455f75301f5e2ae65f44c9522e443c7763d8e))


### Code Refactoring

* discord models are no longer attr classes ([790183e](https://github.com/discatpy-dev/library/commit/790183e54d5e5fc870f829f348e071b95a5aaa56))
* **Flag:** definition of flag members ([ffdb16a](https://github.com/discatpy-dev/library/commit/ffdb16a72e6078f669973d0d009e1422ce9b920c))
* how models are defined ([9bb288e](https://github.com/discatpy-dev/library/commit/9bb288eba11fbd4474877a6fcec6bba8c6547cf6))
* make all models mutable ([0815202](https://github.com/discatpy-dev/library/commit/0815202f327ebc2bf5b7a6e02e68f0df6ad3e6f9))
