#pragma once

#ifdef FIRST_PROJECT_BUILD
#define IMPEXP _declspec(dllexport)
#else
#define IMPEXP _declspec(dllimport)
#endif
