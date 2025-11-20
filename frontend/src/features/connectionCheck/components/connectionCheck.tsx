// frontend/src/components/health-check-button.tsx
import React, { useEffect } from 'react';
import { RefreshCw } from 'lucide-react';
import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import { resetConnectionState, fetchAiConnection, fetchConnection } from "../connectionCheckSlice";
import { selectConnectionStatus, selectBackendConnLoading, selectAiConnectionStatus, selectAiConnLoading } from '../connectionCheckSelectors';
import Button from '../../../components/common/Button';

interface ComponentProps {
  className?: string;
}

const HealthCheckButton: React.FC<ComponentProps> = ({ className }) => {
  const dispatch = useAppDispatch();
  const connection = useAppSelector(selectConnectionStatus);
  const connLoading = useAppSelector(selectBackendConnLoading);
  const aiConnection = useAppSelector(selectAiConnectionStatus);
  const aiConnLoading = useAppSelector(selectAiConnLoading);

  const handleHealthCheck = async () => {
    try {
      await dispatch(fetchConnection());
      // console.log('Backend Service Health:', connection);
      
      await dispatch(fetchAiConnection());
      // console.log('AI Service Health:', aiConnection);
    } catch (error) {
      console.error('Health check failed:', error);
    }
  }

  useEffect(() => {
    dispatch(resetConnectionState());
    handleHealthCheck();
  }, []);

  return (
    <div className={`flex items-center gap-1 text-md ${className}`}>
      <div className='flex flex-col text-sm'>
        <div className='text-sm'>Server: <span>{ (connection === "succeeded")? ((aiConnection === "succeeded")? "Connected" : "Partial" ) : "Disconnected" }</span></div>
      </div>
      <Button 
        className="bg-transparent p-0 m-0 font-bold" 
        onClick={handleHealthCheck} 
        aria-label='Connection Test' 
        disabled={connLoading || aiConnLoading}>
          <RefreshCw className="text-gray-500 dark:text-gray-400" size={16}/>
      </Button>
      {/* <div className='flex flex-col text-sm'>
        <div className='text-sm'>Backend Server: <span>{connection}</span></div>
        <div className='text-sm'>AI Server: <span>{aiConnection}</span></div>
      </div> */}
    </div>
  );
}
export default HealthCheckButton;