// =============================================================================
// PROJECT CHRONO - http://projectchrono.org
//
// Copyright (c) 2014 projectchrono.org
// All right reserved.
//
// Use of this source code is governed by a BSD-style license that can be found
// in the LICENSE file at the top level of the distribution and at
// http://projectchrono.org/license-chrono.txt.
//
// =============================================================================
// Author: Radu Serban
// =============================================================================
//
// =============================================================================

#ifndef ROBO_DRIVER_CB_H
#define ROBO_DRIVER_CB_H

#include "chrono_models/robosimian/robosimian.h"

namespace chrono {
namespace robosimian {

class RobotDriverCallback : public Driver::PhaseChangeCallback {
  public:
    RobotDriverCallback(RoboSimian* robot) : m_robot(robot), m_start_x(0), m_start_time(0) {}
    virtual void OnPhaseChange(Driver::Phase old_phase, Driver::Phase new_phase) override;

    double GetDistance() const { return m_robot->GetChassisPos().x() - m_start_x; }
    double GetDuration() const { return m_robot->GetSystem()->GetChTime() - m_start_time; }
    double GetAvgSpeed() const { return GetDistance() / GetDuration(); }

    double m_start_x;
    double m_start_time;

  private:
    RoboSimian* m_robot;
};

void RobotDriverCallback::OnPhaseChange(Driver::Phase old_phase, Driver::Phase new_phase) {
    if (new_phase == Driver::HOLD) {
        auto& fl = m_robot->GetWheelPos(FL);
        auto& fr = m_robot->GetWheelPos(FR);
        auto& rl = m_robot->GetWheelPos(RL);
        auto& rr = m_robot->GetWheelPos(RR);
        std::cout << "  wheel FL: " << fl.x() << "  " << fl.y() << std::endl;
        std::cout << "  wheel FR: " << fr.x() << "  " << fr.y() << std::endl;
        std::cout << "  wheel RL: " << rl.x() << "  " << rl.y() << std::endl;
        std::cout << "  wheel RR: " << rr.x() << "  " << rr.y() << std::endl;
    }
    if (new_phase == Driver::CYCLE && old_phase != Driver::CYCLE) {
        m_start_x = m_robot->GetChassisPos().x();
        m_start_time = m_robot->GetSystem()->GetChTime();
    }
}

}  // end namespace robosimian
}  // namespace chrono
#endif
