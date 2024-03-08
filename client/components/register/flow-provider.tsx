'use client';
import useRegisterFlow from '@/lib/hooks/useRegisterFlow';
import { createContext, useContext } from 'react';

interface RegisterFlowContextType {
  flow: { email: string; currentStep: string; id: string } | null;
}

const RegisterFlowContext = createContext<RegisterFlowContextType>({
  flow: null,
});

export const useLocalRegisterFlow = () => useContext(RegisterFlowContext);

interface RegisterFlowProviderProps {
  flow: { email: string; currentStep: string; id: string } | null;
}

export const LocalRegisterFlowProvider: React.FC<
  React.PropsWithChildren<RegisterFlowProviderProps>
> = ({ children, flow }) => {
  let localFlow = null;

  if (flow) {
    // FIXME we are conditionally calling this hook, thats the issue!
    // we won't be encountering these issues if we use a cookie that doesn't need to be
    // explicitly passed over every request (like a session cookie), and we can omit the
    // path parameters!!
    const { data } = useRegisterFlow({ flowId: flow.id }, flow);
    if (data) {
      localFlow = data;
    }
  }
  return (
    <RegisterFlowContext.Provider
      value={{
        flow: localFlow,
      }}
    >
      {children}
    </RegisterFlowContext.Provider>
  );
};
