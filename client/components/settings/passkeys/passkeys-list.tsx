'use client';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import useWebAuthnCredentials from '@/lib/hooks/useWebAuthnCredentials';

export default function PasskeysList() {
  const webAuthnCredentials = useWebAuthnCredentials();

  return (
    <div className='flex flex-col gap-4'>
      {webAuthnCredentials.data.map((credential) => (
        <Card key={credential.id}>
          <CardHeader>{credential.deviceType}</CardHeader>
          <CardContent>
            <div className='flex flex-col gap-4'>
              <p>{credential.credentialId}</p>
              <p>{credential.publicKey}</p>
              {/* <p>{credential.createdAt}</p> */}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
