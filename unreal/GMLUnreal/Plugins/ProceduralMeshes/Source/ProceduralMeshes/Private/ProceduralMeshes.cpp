// Copyright 2016, Sigurdur Gunnarsson. All Rights Reserved. 

#include "ProceduralMeshesPrivatePCH.h"

#define LOCTEXT_NAMESPACE "FProceduralMeshesModule"

void FProceduralMeshesModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
}

void FProceduralMeshesModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FProceduralMeshesModule, ProceduralMeshes)