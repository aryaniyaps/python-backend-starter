'use client';
import { createContext, useContext, useState } from 'react';

interface RegisterFlowContextType {
  setCurrentStep: (step: string | null) => void;
  currentStep: string | null;
  flowData: { email: string; currentStep: string; id: string } | undefined;
}

// TODO: pass register flow email here
const RegisterFlowContext = createContext<RegisterFlowContextType>({
  setCurrentStep(step) {},
  currentStep: null,
  flowData: undefined,
});

export const useRegisterFlow = () => useContext(RegisterFlowContext);

interface RegisterFlowProviderProps {
  flowData: { email: string; currentStep: string; id: string } | undefined;
}

export const RegisterFlowProvider: React.FC<
  React.PropsWithChildren<RegisterFlowProviderProps>
> = ({ children, flowData }) => {
  const [localCurrentStep, setCurrentStep] = useState<string | null>(
    flowData ? flowData.currentStep : null
  );

  return (
    <RegisterFlowContext.Provider
      value={{
        setCurrentStep,
        currentStep: localCurrentStep,
        flowData,
      }}
    >
      {children}
    </RegisterFlowContext.Provider>
  );
};
