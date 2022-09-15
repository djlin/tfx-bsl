# Updates

* Remove in .bazelrc (removed in 5.0)

    #build --incompatible_restrict_string_escapes=false

* Modify the followings under /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/commands_overloads/

    default_commands.bzl

    osx_commands.bzl

    linux_commands.bzl

    windows_commands.bzl

    * Mainly, (remove \ before \$) (remove \( and \) in find)

        _REPLACE_VALUE = "${EXT_BUILD_DEPS}"

        58   find -L $1 -type f \
        59    -name "*.pc" -or -name "*.la" -or -name "*-config" -or -name "*.cmake" \
        60   -exec sed -i 's@'"$2"'@'"$3"'@g' {} ';'

* Fix ln (no -t option under Mac OS X)

    if [[ -d $1 ]]; then
      local dir_name="$(basename "$1")"
      ln -s $1 ${target}/${dir_name}
      #ln -s -t ${target} $1
    elif [[ -f $1 ]]; then
      ln -s -t $1 ${target}
      #ln -s -t ${target} $1

* Not necessarily useful, but...


        https://github.com/tensorflow/tfx-bsl/commit/c60fb04aa63d953bd58ab219a463b8d47036ba93

        https://github.com/bazelbuild/rules_foreign_cc/releases


* Change in /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/com_google_zetasql/bazel/zetasql_deps_step_2.bzl
  
        24 #load("@rules_foreign_cc//:workspace_definitions.bzl", "rules_foreign_cc_dependencies")
        25 load("@rules_foreign_cc//foreign_cc:repositories.bzl", "rules_foreign_cc_dependencies")

* Add /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/com_google_zetasql/WORKSPACE

        3 load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
        4
        5 http_archive(
        6     name = "rules_foreign_cc",
        7     sha256 = "2a4d07cd64b0719b39a7c12218a3e507672b82a97b98c6a89d38565894cf7c51",
        8     strip_prefix = "rules_foreign_cc-0.9.0",
        9     url = "https://github.com/bazelbuild/rules_foreign_cc/archive/refs/tags/0.9.0.tar.gz",
        10 )
        11
        12 load("@rules_foreign_cc//foreign_cc:repositories.bzl", "rules_foreign_cc_dependencies")

* Change /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/com_google_zetasql/bazel/icu.BUILD

        21 #load("@rules_foreign_cc//tools/build_defs:configure.bzl", "configure_make")
        22 load("@rules_foreign_cc//foreign_cc:configure.bzl", "configure_make")

* Change /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/com_google_zetasql/bazel/BUILD

        21 #load("@rules_foreign_cc//tools/build_defs:configure.bzl", "configure_make")
        22 load("@rules_foreign_cc//foreign_cc:configure.bzl", "configure_make")

        43     #binaries = [
        44     out_binaries = [
 
        47     #configure_env_vars = {
        48     env = {

        65     #binaries = [
        66     out_binaries = [    

        71     #configure_env_vars = {
        72     env = {

        # caused unbound variable error
        74     #    "CC_FOR_BUILD": "$$CC$$",

        76     #static_libraries = ["liby.a"],
        77     out_static_libs = ["liby.a"],

        90     # binaries = [
        91     out_binaries = [

        99     #configure_env_vars = {
        100     env = {

* Change /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/com_google_zetasql/bazel/zetasql_deps_step_2.bzl

        24 #load("@rules_foreign_cc//:workspace_definitions.bzl", "rules_foreign_cc_dependencies")
        25 load("@rules_foreign_cc//foreign_cc:repositories.bzl", "rules_foreign_cc_dependencies")

* Add in /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/com_google_zetasql/bazel/flex.bzl

        62 load("@rules_foreign_cc//foreign_cc:configure.bzl", "configure_make")

* Change /private/var/tmp/_bazel_tachun/cd952155e8308a0b7772c90228e504a3/external/icu/BUILD.bazel

        21 #load("@rules_foreign_cc//tools/build_defs:configure.bzl", "configure_make")
        22 load("@rules_foreign_cc//foreign_cc:configure.bzl", "configure_make")

        39     #configure_env_vars = {
        40     env = {

        59     #static_libraries = [
        60     out_static_libs = [

        # caused unbound variable error
        43         #"LIBS": "$$LDFLAGS$$",
        