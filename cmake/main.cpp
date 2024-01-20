//
// Created by BillHu on 2020/11/12.
//
#include <iostream>
#include <vector>
// #include "gfunc.h"
#include "PQX.h"
#include <iomanip>

int main(int argc, char *argv[]) {
    PQX fu = PQX(L"D:\\SmartRoadBridgePy\\cmake\\D1.ICD");
    Vector cc = fu.get_dir(10);
    std::wcout << std::fixed << std::setprecision(8) << cc[0] << ",";
    std::wcout << std::fixed << std::setprecision(8) << cc[1] << std::endl;
}