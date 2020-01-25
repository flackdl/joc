import React from 'react';
import './App.css';
import  { Search } from './search/Search';

function App() {
  return (
    <div className={'container'}>
        <Search placeholder={'vegetable souffle'} />
    </div>
  );
}

export default App;
