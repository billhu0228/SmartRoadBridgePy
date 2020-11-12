//
// Created by BillHu on 2020/11/12.
//
#include <iostream>
#include <vector>
#include "gfunc.h"


int main(int argc, char *argv[]) {
    std::vector<double> f = intersection_seg_arc(472408.5956773032, 9856940.507514307, 1393.499999530321,
                                            471151.5248327673, 9856303.181315701,
                                            471241.8886555169, 9856346.010972928
    );
    std::cout << std::to_string(f[0]) << std::endl;
}