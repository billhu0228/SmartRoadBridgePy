//
// Created by BillHu on 2020/11/12.
//
#include <iostream>
#include <vector>
// #include "gfunc.h"
#include "PQX.h"
#include <iomanip>

int main(int argc, char *argv[]) {
    PQX fu = PQX(L"E:\\20191213-�����Ǹ߼���ʩ��ͼ���(19406)\\20221208 HSI�½��ѵ���\\python\\Z-1208\\Z-1208.ICD");
    Vector cc = fu.get_dir(400);
    std::wcout << std::fixed << std::setprecision(8) << cc[0] << ",";
    std::wcout << std::fixed << std::setprecision(8) << cc[1] << std::endl;
}