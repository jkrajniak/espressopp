/*
  Copyright (C) 2021
      Max Planck Institute for Polymer Research & JGU Mainz

  This file is part of ESPResSo++.

  ESPResSo++ is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  ESPResSo++ is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// ESPP_CLASS
#ifndef VEC_INTEGRATOR_VELOCITYVERLET_HPP
#define VEC_INTEGRATOR_VELOCITYVERLET_HPP

#include "vec/include/types.hpp"
#include "vec/integrator/MDIntegratorVec.hpp"
#include "types.hpp"
#include "integrator/MDIntegrator.hpp"
#include "esutil/Timer.hpp"
#include <boost/signals2.hpp>

namespace espressopp { namespace vec {
  namespace integrator {

    /// Velocity Verlet Integrator
    class VelocityVerlet
      : public MDIntegratorVec
    {
    public:
      typedef espressopp::integrator::MDIntegrator MDIntegrator;
      typedef espressopp::vec::integrator::MDIntegratorVec MDIntegratorVec;

      VelocityVerlet(
        shared_ptr<Vectorization> vectorization
        );

      virtual void run(int nsteps);

      real getTimeStep() { return MDIntegratorVec::getTimeStep(); }

      /// Load timings in array to export to Python as a tuple
      void loadTimers(real t[10]);

      /// Reset timers to zero
      void resetTimers();

      /// Returns the number of resorts done during a single call to integrator.run().
      /// Its value is reset to zero at the beginning of each run
      int getNumResorts() const;

      /// Register this class so it can be used from Python
      static void registerPython();

    protected:

      bool resortFlag;  //!< true implies need for resort of particles
      int nResorts;
      real maxDist;
      real maxCut;

      real integrate1();

      void integrate2();

      void calcForces();

      void updateForces();

      // void updateForcesBlock();

      void initForcesPlist();

      void initForcesParray();

      espressopp::esutil::WallTimer timeIntegrate;  //!< used for timing

      // variables that keep time information about different phases
      real timeRun;
      real timeLost;
      real timeForce;
      real timeForceComp[100];
      real timeComm1;
      real timeComm2;
      real timeInt1;
      real timeInt2;
      real timeResort;

      static LOG4ESPP_DECL_LOGGER(theLogger);
    };

  }
}}

#endif//VEC_INTEGRATOR_VELOCITYVERLET_HPP
