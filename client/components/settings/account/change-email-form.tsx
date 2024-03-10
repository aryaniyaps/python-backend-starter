'use client';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import useCurrentUser from '@/lib/hooks/useCurrentUser';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const changeEmailSchema = z.object({
  email: z.string().email(),
});

export default function ChangeEmailForm() {
  const { data: user } = useCurrentUser();

  const form = useForm<z.infer<typeof changeEmailSchema>>({
    resolver: zodResolver(changeEmailSchema),
    defaultValues: {
      email: user.email,
    },
  });

  async function onSubmit(values: z.infer<typeof changeEmailSchema>) {}

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className='flex w-full items-start gap-4'
      >
        <div className='flex w-96 flex-col gap-4'>
          <FormField
            control={form.control}
            name='email'
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <Input disabled {...field} />
                </FormControl>
                <FormDescription>
                  Your email address is private.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
      </form>
    </Form>
  );
}
