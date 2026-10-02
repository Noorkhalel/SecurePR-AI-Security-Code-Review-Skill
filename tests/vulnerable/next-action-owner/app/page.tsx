import { removeDocument } from './actions';
export default function Page() {
  return <form action={removeDocument.bind(null, 'doc-public-id')}><button>Delete</button></form>;
}
