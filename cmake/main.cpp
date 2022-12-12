//
// Created by BillHu on 2020/11/12.
//
#include <iostream>
#include <vector>
// #include "gfunc.h"
#include "PQX.h"
#include <iomanip>

int main(int argc, char *argv[]) {
    PQX fu = PQX(L"E:\\20191213-肯尼亚高架桥施工图设计(19406)\\20221208 HSI新建匝道桥\\python\\Z-1208\\Z-1208.ICD");
    Vector cc = fu.get_dir(400);
    std::wcout << std::fixed << std::setprecision(8) << cc[0] << ",";
    std::wcout << std::fixed << std::setprecision(8) << cc[1] << std::endl;
}