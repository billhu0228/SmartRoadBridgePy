//
// Created by IBD2 on 2020/10/29.
//
#include <iostream>
#include "PQX.h"

int main(int argc, char *argv[]) {
    PQX A8L = PQX("../A8L2.icd");
    std::cout << A8L.get_station_by_point(476761.9165, 9853244.2433, 20, 1e-9);
    return 0;
}

