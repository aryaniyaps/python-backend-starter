import AppearanceForm from '@/components/settings/appearance/appearance-form';

export default function AppearanceSettingsPage() {
  return (
    <div className='space-y-6'>
      <div className='flex flex-col'>
        <h3 className='text-lg font-medium'>Appearance</h3>
        <p className='text-sm text-muted-foreground'>
          Manage how your app looks here.
        </p>
      </div>
      <AppearanceForm />
    </div>
  );
}
