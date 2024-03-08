import { LocalRegisterFlowProvider } from '@/components/register/flow-provider';

export default function RegisterLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <LocalRegisterFlowProvider>{children}</LocalRegisterFlowProvider>;
}
