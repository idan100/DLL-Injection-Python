// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"



BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
	killProcessByName("chrome.exe");
	createProccessByName("C:\\Program Files(x86)\\Microsoft\\Edge\\Application\\msedge.exe");

    return TRUE;
}

