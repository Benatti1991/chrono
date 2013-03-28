#ifndef CH_SYSTEMGPU_H
#define CH_SYSTEMGPU_H
//////////////////////////////////////////////////
//
//   ChSystemGPU.h
//
//   GPU Simulation System
//
//   HEADER file for CHRONO,
//   Multibody dynamics engine
//
// ------------------------------------------------
//   Copyright:Alessandro Tasora / DeltaKnowledge
//             www.deltaknowledge.com
// ------------------------------------------------
///////////////////////////////////////////////////
#include "ChCudaMath.h"
#include "ChCudaDefines.h"
#include <stdlib.h>
#include <float.h>
#include <memory.h>
#include <algorithm>
#include "core/ChTimer.h"
#include "physics/ChSystem.h"
#include "physics/ChGlobal.h"
#include "physics/ChContactContainer.h"
#include "ChLcpSolverGPU.h"
#include "ChLcpSystemDescriptorGPU.h"
#include "ChDataManager.h"
#include "collision/ChCCollisionSystemGPU.h"

namespace chrono {
	using namespace chrono;

	class ChApiGPU ChSystemGPU: public ChSystem {
		CH_RTTI(ChSystemGPU, ChObj)
			;

		public:
			ChSystemGPU(unsigned int max_objects = 1000);
			virtual int Integrate_Y_impulse_Anitescu();
			double ComputeCollisions();
			double SolveSystem();
			double SplitData();
			void AddBody(ChSharedPtr<ChBodyGPU> newbody);
			void RemoveBody(ChSharedPtr<ChBodyGPU> mbody);
			void RemoveBody(int i);
			int Setup();
			void Update();
			void ChangeCollisionSystem(ChCollisionSystem *newcollsystem);
			void ChangeLcpSolverSpeed(ChLcpSolver *newsolver);
			int GetNcontacts() {
				return gpu_data_manager->number_of_contacts;
			}
			double GetTimerCollision() {
				return timer_collision;
			}
			ChGPUDataManager *gpu_data_manager;
		private:
			ChTimer<double> mtimer_lcp, mtimer_step, mtimer_cd_broad, mtimer_cd_narrow, mtimer_cd, mtimer_updt;
			unsigned int counter;
			double timer_collision;
			std::list<ChLink *>::iterator it;
	};
}

#endif

