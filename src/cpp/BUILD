cc_binary(
    name = "00",
    srcs = ["00.cpp"]
)

cc_binary(
    name = "01",
    srcs = ["01.cpp"]
)

cc_binary(
    name = "01_ylks",
    srcs = ["01_ylks.cpp"],
    deps = [
        "//src/cpp/third_parties/CLI11:CLI11",
        "//src/cpp/shared_libs/io_utils:io_utils"
    ],
    copts = [
        "-std=c++17",
        "-lstdc++fs"
    ]
)

cc_binary(
    name = "02_rk",
    srcs = ["02_rk.cpp"],
    copts = [
        "-std=c++20",
    ]
)
