import PasskeysList from '@/components/settings/passkeys/passkeys-list';
import { Button } from '@/components/ui/button';

export default function PasskeysSettingsPage() {
  return (
    <div className='space-y-6'>
      <div className='flex w-full justify-between gap-4'>
        <div className='flex flex-col'>
          <h3 className='text-lg font-medium'>Passkeys</h3>
          <p className='text-sm text-muted-foreground'>
            Manage your passkeys here.
          </p>
        </div>
        <Button>Add passkey</Button>
      </div>
      <PasskeysList />
    </div>
  );
}
