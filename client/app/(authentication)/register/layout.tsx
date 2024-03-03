import { RegisterFlowProvider } from '@/components/register-flow-provider';

export default function RegisterLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <RegisterFlowProvider>{children}</RegisterFlowProvider>;
}
