'use client';
import { components } from '@/generated/api/v1';
import { client } from '@/lib/client';
import { useRouter } from 'next/navigation';
import { createContext, useContext, useEffect, useState } from 'react';

type RegisterFlowStep = components['schemas']['RegisterFlowStep'];

interface RegisterFlowContextType {
  currentStep: RegisterFlowStep | null;
  setCurrentStep: (step: RegisterFlowStep | null) => void;
  flowId: string | null;
  setFlowId: (flowId: string | null) => void;
}

// TODO: pass register flow email here
const RegisterFlowContext = createContext<RegisterFlowContextType>({
  currentStep: null,
  setCurrentStep(step) {},
  flowId: null,
  setFlowId(flowId) {},
});

export const useRegisterFlow = () => useContext(RegisterFlowContext);

export const RegisterFlowProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [currentStep, setCurrentStep] = useState<RegisterFlowStep | null>(null);
  const [flowId, setLocalFlowId] = useState<string | null>(null);
  const router = useRouter();

  const setFlowId = (flowId: string | null) => {
    if (flowId) {
      localStorage.setItem('flowId', flowId);
    } else {
      localStorage.removeItem('flowId');
    }
    setLocalFlowId(flowId);
  };

  useEffect(() => {
    // Check if window is defined to ensure client-side execution
    if (typeof window !== 'undefined') {
      const localFlowId = localStorage.getItem('flowId');
      setLocalFlowId(localFlowId);
    }
  }, []);

  useEffect(() => {
    if (flowId) {
      if (!currentStep) {
        client
          .GET('/auth/register/flows/{flow_id}', {
            params: { path: { flow_id: flowId } },
          })
          .then(({ data }) => {
            if (data) {
              setCurrentStep(data.currentStep);
            }
          })
          .catch((error) => {
            console.error('Error fetching flow data:', error);
            // Handle error if needed
            setFlowId(null);
          });
      }

      switch (currentStep) {
        case 'email_verification':
          router.push('/register/verification');
          break;
        case 'webauthn_start':
          router.push('/register/webauthn');
          break;
        case 'webauthn_finish':
          router.push('/register/webauthn');
          break;
        default:
          console.error('current step not found!');
          break;
      }
    } else {
      router.push('/register');
    }
  }, [flowId, currentStep]);

  return (
    <RegisterFlowContext.Provider
      value={{ currentStep, setCurrentStep, flowId, setFlowId }}
    >
      {children}
    </RegisterFlowContext.Provider>
  );
};
