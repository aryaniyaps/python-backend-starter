'use client';
import { createContext, useContext, useState } from 'react';

interface RegisterFlowContextType {
  setCurrentStep: (step: string | null) => void;
  currentStep: string | null;
  flow: { email: string; currentStep: string; id: string } | null;
  setFlow: (flow: { email: string; currentStep: string; id: string }) => void;
}

const RegisterFlowContext = createContext<RegisterFlowContextType>({
  setCurrentStep(step) {},
  currentStep: null,
  setFlow(flow) {},
  flow: null,
});

export const useRegisterFlow = () => useContext(RegisterFlowContext);

interface RegisterFlowProviderProps {
  flow: { email: string; currentStep: string; id: string } | null;
}

export const RegisterFlowProvider: React.FC<
  React.PropsWithChildren<RegisterFlowProviderProps>
> = ({ children, flow }) => {
  const [localFlow, setFlow] = useState<{
    email: string;
    currentStep: string;
    id: string;
  } | null>(flow ? flow : null);
  const [localCurrentStep, setCurrentStep] = useState<string | null>(
    flow ? flow.currentStep : null
  );

  return (
    <RegisterFlowContext.Provider
      value={{
        setCurrentStep,
        currentStep: localCurrentStep,
        flow: localFlow,
        setFlow,
      }}
    >
      {children}
    </RegisterFlowContext.Provider>
  );
};
