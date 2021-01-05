//
// Created by BillHu on 2020/11/12.
//
#include <iostream>
#include <vector>
// #include "gfunc.h"
#include "PQX.h"

int main(int argc, char *argv[]) {
    PQX fu = PQX(L"G:\\20191213-肯尼亚高架桥施工图设计(19406)\\01 前方资料\\EI Data\\00-MainLine\\L1K-0926\\L1K-0926.ICD");
    double kk=fu.get_station_by_point2(470989.6093,9856656.7479,471011.6007,9856673.0456);
    Vector cc=fu.get_coordinate(kk);
    std::wcout << cc[0]<<","<<cc[1]<< std::endl;
}