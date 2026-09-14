import React from 'react';
import { X, HelpCircle, Mail, MessageSquare, Phone } from 'lucide-react';

interface HelpSupportModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function HelpSupportModal({ isOpen, onClose }: HelpSupportModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-lg w-full overflow-hidden animate-fade-in-up border-2 border-[#003366]">
        <div className="bg-[#003366] text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <HelpCircle size={24} />
            <h2 className="text-xl font-bold font-mono">NORVAULT Support</h2>
          </div>
          <button onClick={onClose} className="hover:bg-white/20 p-1 rounded-full transition-colors">
            <X size={24} />
          </button>
        </div>
        
        <div className="p-6 space-y-6">
          <p className="text-gray-600">
            Welcome to the NORVAULT Company Intelligence Engine. If you need assistance with the competition parameters, verification logic, or system architecture, we are here to help.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border border-gray-200 p-4 rounded-lg hover:border-[#003366] transition-colors cursor-pointer group">
              <MessageSquare className="text-[#003366] mb-2 group-hover:scale-110 transition-transform" size={28} />
              <h3 className="font-bold text-gray-900">Live Chat</h3>
              <p className="text-sm text-gray-500 mt-1">Chat with a verification expert instantly.</p>
            </div>
            
            <div className="border border-gray-200 p-4 rounded-lg hover:border-[#003366] transition-colors cursor-pointer group">
              <Mail className="text-[#003366] mb-2 group-hover:scale-110 transition-transform" size={28} />
              <h3 className="font-bold text-gray-900">Email Support</h3>
              <p className="text-sm text-gray-500 mt-1">Get detailed technical assistance.</p>
            </div>
            
            <div className="border border-gray-200 p-4 rounded-lg hover:border-[#003366] transition-colors cursor-pointer group">
              <Phone className="text-[#003366] mb-2 group-hover:scale-110 transition-transform" size={28} />
              <h3 className="font-bold text-gray-900">Priority Call</h3>
              <p className="text-sm text-gray-500 mt-1">Available for enterprise competition tier.</p>
            </div>

            <div className="border border-gray-200 p-4 rounded-lg bg-gray-50">
              <h3 className="font-bold text-gray-900">Documentation</h3>
              <ul className="text-sm text-[#003366] mt-2 space-y-1 list-disc list-inside">
                <li><a href="#" className="hover:underline">Verification Logic</a></li>
                <li><a href="#" className="hover:underline">BRREG Integrations</a></li>
                <li><a href="#" className="hover:underline">Adversarial Audits</a></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
          <button 
            onClick={onClose}
            className="px-6 py-2 bg-[#003366] text-white rounded font-medium hover:bg-[#002244] transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
