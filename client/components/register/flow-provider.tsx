'use client';
import { createContext, useContext, useState } from 'react';

interface RegisterFlowContextType {
  setCurrentStep: (step: string | null) => void;
  currentStep: string | null;
  flow: { email: string; currentStep: string; id: string } | undefined;
}

// TODO: pass register flow email here
const RegisterFlowContext = createContext<RegisterFlowContextType>({
  setCurrentStep(step) {},
  currentStep: null,
  flow: undefined,
});

export const useRegisterFlow = () => useContext(RegisterFlowContext);

interface RegisterFlowProviderProps {
  flow: { email: string; currentStep: string; id: string } | undefined;
}

export const RegisterFlowProvider: React.FC<
  React.PropsWithChildren<RegisterFlowProviderProps>
> = ({ children, flow }) => {
  const [localCurrentStep, setCurrentStep] = useState<string | null>(
    flow ? flow.currentStep : null
  );

  return (
    <RegisterFlowContext.Provider
      value={{
        setCurrentStep,
        currentStep: localCurrentStep,
        flow,
      }}
    >
      {children}
    </RegisterFlowContext.Provider>
  );
};
