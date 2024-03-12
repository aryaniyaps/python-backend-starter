import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Form } from '@/components/ui/form';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { APP_NAME, MAX_EMAIL_LENGTH } from '@/lib/constants';
import useAuthenticateStart from '@/lib/hooks/useAuthenticateStart';
import { zodResolver } from '@hookform/resolvers/zod';
import { DialogClose } from '@radix-ui/react-dialog';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const changeEmailSchema = z.object({
  newEmail: z
    .string()
    .min(1, { message: 'Email address is required' })
    .email({ message: 'Email address is invalid' })
    .max(MAX_EMAIL_LENGTH),
});

export default function RevokeSessionDialog() {
  const form = useForm({
    resolver: zodResolver(changeEmailSchema),
    defaultValues: { newEmail: '' },
  });

  const authenticateStart = useAuthenticateStart();

  async function onSubmit(values: z.infer<typeof changeEmailSchema>) {
    try {
      // start webauthn authentication
      // FIXME: we need an API method to re authenticate without requiring email
      const data = await authenticateStart.mutateAsync({ email: '' });
    } catch (err) {
      // TODO: handle errors better
    }
  }

  return (
    <Dialog>
      <Tooltip>
        <TooltipTrigger asChild>
          <span>
            <DialogTrigger asChild>
              <Button size='icon' variant='destructive'>
                <Icons.trash className='h-4 w-4' />
              </Button>
            </DialogTrigger>
          </span>
        </TooltipTrigger>
        <TooltipContent>Revoke session</TooltipContent>
      </Tooltip>
      <DialogContent className='sm:max-w-[475px]'>
        <DialogHeader>
          <DialogTitle>Revoke session</DialogTitle>
          <DialogDescription>
            This will remove access to your {APP_NAME} account from the device
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex w-full flex-col gap-6'
          >
            <DialogFooter className='flex w-full items-end gap-4'>
              <DialogClose asChild>
                <Button variant='ghost'>Cancel</Button>
              </DialogClose>
              <Button type='submit'>Confirm</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
