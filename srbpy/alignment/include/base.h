#pragma once
#include <fstream>
#include <iostream>
#include <vector>

std::wstring utf8_to_utf16(const std::string& utf8);

struct BPD
{
	double pk;
	double elevation;
	double radius;
};

struct CGD
{
	double pk;
	double l_slope,r_slope;	
};

struct RCD
{
	double pk;
	double elevation;	
};