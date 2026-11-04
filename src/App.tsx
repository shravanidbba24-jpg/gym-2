import React, { useState, useEffect, useMemo } from 'react';
import {
  Dumbbell,
  Flame,
  HeartPulse,
  Activity,
  CheckCircle2,
  AlertCircle,
  Terminal,
  ExternalLink,
  Copy,
  Check,
  Search,
  Plus,
  Trash2,
  Download,
  RefreshCw,
  Clock,
  MapPin,
  Phone,
  Mail,
  User,
  ShieldCheck,
  Utensils,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  Calculator,
  Calendar,
  Zap,
  ArrowUpRight,
  Code2,
  Monitor
} from 'lucide-react';

interface Member {
  id: string;
  name: string;
  email: string;
  phone: string;
  program: string;
  time_slot: string;
  tier: string;
  branch: string;
  joined_at: string;
}

const INITIAL_MEMBERS: Member[] = [
  {
    id: "FIT-1042",
    name: "Rahul Sharma",
    email: "rahul.s@example.com",
    phone: "+91 98201 92834",
    program: "Weight Training",
    time_slot: "Morning (06:00 - 09:00)",
    tier: "Pro Member",
    branch: "Pune - Koregaon Park (Flagship)",
    joined_at: "02 Nov 2026, 09:14 AM"
  },
  {
    id: "FIT-1041",
    name: "Sneha Patel",
    email: "sneha.p@example.com",
    phone: "+91 98202 84729",
    program: "Cardio Training",
    time_slot: "Evening (17:00 - 21:00)",
    tier: "Elite All-Access",
    branch: "Pune - Baner High Street",
    joined_at: "01 Nov 2026, 04:30 PM"
  },
  {
    id: "FIT-1040",
    name: "Amit Kumar",
    email: "amit.k@example.com",
    phone: "+91 98203 19482",
    program: "Weight Training",
    time_slot: "Morning (06:00 - 09:00)",
    tier: "Pro Member",
    branch: "Pune - Koregaon Park (Flagship)",
    joined_at: "30 Oct 2026, 11:20 AM"
  },
  {
    id: "FIT-1039",
    name: "Kavita Verma",
    email: "kavita@example.com",
    phone: "+91 98204 38291",
    program: "Yoga & Mobility",
    time_slot: "Morning (06:00 - 09:00)",
    tier: "Pro Member",
    branch: "Pune - Koregaon Park (Flagship)",
    joined_at: "28 Oct 2026, 07:45 AM"
  }
];

// Programs from the Python Tkinter app
const PROGRAMS_DATA = [
  {
    id: "p1",
    title: "Weight Training",
    desc: "Build muscles with professional trainers.",
    more: "Weight training includes Olympic bench press, squats, deadlifts and progressive overload. Helps increase lean muscle density, metabolic rate and physical power.",
    tag: "High Intensity • Eleiko Power Racks",
    image: "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&auto=format&fit=crop&q=80"
  },
  {
    id: "p2",
    title: "Cardio Training",
    desc: "Improve stamina and heart health.",
    more: "Cardio exercises like running, cycling and curved treadmills help burn calories and improve heart health with zone-2 to zone-5 conditioning.",
    tag: "Aerobic Capacity • Heart Rate Telemetry",
    image: "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800&auto=format&fit=crop&q=80"
  },
  {
    id: "p3",
    title: "Yoga & Mobility",
    desc: "Relax your mind and restore body balance.",
    more: "Yoga improves flexibility, reduces stress, decompresses joints and helps maintain mental clarity and athletic spinal longevity.",
    tag: "Restorative • Rishikesh Masters",
    image: "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=800&auto=format&fit=crop&q=80"
  }
];

// Services from the Python Tkinter app
const SERVICES_DATA = [
  {
    id: "s1",
    title: "Personal Training",
    desc: "1 to 1 training with certified trainers.",
    more: "Our trainers create personalized workout plans based on your body goals with biometric tracking and kinematic assessments.",
    badge: "1-on-1 Biomechanical Coaching"
  },
  {
    id: "s2",
    title: "Diet Plan & Nutrition",
    desc: "Professional diet plans for fitness goals.",
    more: "Healthy diet charts prepared by sports nutrition experts to support clean muscle growth, fat loss, and micronutrient balance.",
    badge: "Desi High-Protein Diet Plans"
  },
  {
    id: "s3",
    title: "Modern Equipment",
    desc: "Latest gym machines and equipment.",
    more: "Our gym uses advanced Eleiko calibrated barbells, pneumatic machines, and Finnish sauna recovery suites for safe and effective workouts.",
    badge: "Olympic Hardware & Sauna"
  }
];

// Reviews from the Python Tkinter app
const REVIEWS_DATA = [
  {
    id: "r1",
    name: "Rahul",
    avatar: "R",
    quote: '"Best gym in the city."',
    more: "Rahul improved strength in 6 months. Bench press increased by 35kg while keeping body fat lean.",
    branch: "Pune - Koregaon Park"
  },
  {
    id: "r2",
    name: "Sneha",
    avatar: "S",
    quote: '"Great environment."',
    more: "Sneha loves the trainers and equipment. Prepared for the Pune half-marathon with zero joint pain.",
    branch: "Pune - Baner High St"
  },
  {
    id: "r3",
    name: "Amit",
    avatar: "A",
    quote: '"I lost 10kg."',
    more: "Amit followed the cardio and diet plan regularly. Dropped 10kg clean fat in 4 months.",
    branch: "Pune - Koregaon Park"
  }
];

export default function App() {
  // Members State
  const [members, setMembers] = useState<Member[]>(() => {
    const saved = localStorage.getItem('fg_pune_members');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        return INITIAL_MEMBERS;
      }
    }
    return INITIAL_MEMBERS;
  });

  // Expandable Card States (matches Tkinter info_card toggles!)
  const [expandedPrograms, setExpandedPrograms] = useState<Record<string, boolean>>({});
  const [expandedServices, setExpandedServices] = useState<Record<string, boolean>>({});
  const [expandedReviews, setExpandedReviews] = useState<Record<string, boolean>>({});

  // Search & Filter
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBranchFilter, setSelectedBranchFilter] = useState('ALL');

  // Form State (matching Tkinter contact form: name, email, phone)
  const [formName, setFormName] = useState('');
  const [formEmail, setFormEmail] = useState('');
  const [formPhone, setFormPhone] = useState('');
  const [formProgram, setFormProgram] = useState('Weight Training');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null);

  // Digital Pass Modal
  const [activePassMember, setActivePassMember] = useState<Member | null>(null);

  // Modals & Panels
  const [showVercelModal, setShowVercelModal] = useState(false);
  const [showPythonScriptModal, setShowPythonScriptModal] = useState(false);
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'offline'>('checking');
  const [apiResponseInfo, setApiResponseInfo] = useState<string>('');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  // Diet Plan Active Tab
  const [dietTab, setDietTab] = useState<'veg' | 'nonveg'>('veg');

  // BMI Calculator State
  const [bmiWeight, setBmiWeight] = useState<number>(72);
  const [bmiHeight, setBmiHeight] = useState<number>(175);
  const [bmiGoal, setBmiGoal] = useState<'muscle' | 'fatloss' | 'endurance'>('muscle');

  // Sync to localStorage
  useEffect(() => {
    localStorage.setItem('fg_pune_members', JSON.stringify(members));
  }, [members]);

  // Check Backend / Vercel API Health
  const checkApiHealth = async () => {
    setApiStatus('checking');
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setApiStatus('connected');
        setApiResponseInfo(`Connected to ${data.service || 'Vercel Python API'} (${data.environment || 'live'})`);
      } else {
        setApiStatus('offline');
        setApiResponseInfo('HTTP ' + res.status + ' - Using client-side persistence mode');
      }
    } catch (err) {
      setApiStatus('offline');
      setApiResponseInfo('Local preview / Serverless offline - Using client fallback');
    }
  };

  useEffect(() => {
    checkApiHealth();
  }, []);

  // Copy helper
  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(id);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  // Toggle helpers
  const toggleProgram = (id: string) => {
    setExpandedPrograms(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const toggleService = (id: string) => {
    setExpandedServices(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const toggleReview = (id: string) => {
    setExpandedReviews(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // BMI calculation
  const bmiResult = useMemo(() => {
    if (!bmiHeight || !bmiWeight) return null;
    const heightInMeters = bmiHeight / 100;
    const bmi = +(bmiWeight / (heightInMeters * heightInMeters)).toFixed(1);
    let category = '';
    let color = '';
    let recommendation = '';

    if (bmi < 18.5) {
      category = 'Underweight (कम वजन)';
      color = 'text-amber-400';
      recommendation = 'Focus on caloric surplus with Shakahari High-Protein diet & Olympic Weight Training.';
    } else if (bmi <= 22.9) {
      category = 'Normal / Athletic Range (सामान्य)';
      color = 'text-emerald-400';
      recommendation = 'Optimal body composition. Maintain with progressive overload & zone-2 cardio.';
    } else if (bmi <= 24.9) {
      category = 'Overweight Risk (अधिक वजन)';
      color = 'text-amber-500';
      recommendation = 'Aim for mild caloric deficit with Cardio HIIT and Lean Muscle diet plan.';
    } else {
      category = 'Obesity (मोटापा)';
      color = 'text-rose-400';
      recommendation = 'Target structured fat loss with personal coaching and endurance intervals.';
    }

    let dailyCalories = 2200;
    if (bmiGoal === 'muscle') dailyCalories = Math.round(bmiWeight * 33 + 400);
    if (bmiGoal === 'fatloss') dailyCalories = Math.round(bmiWeight * 28 - 400);
    if (bmiGoal === 'endurance') dailyCalories = Math.round(bmiWeight * 32);

    return { bmi, category, color, recommendation, dailyCalories };
  }, [bmiWeight, bmiHeight, bmiGoal]);

  // Handle Join Form Submit
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName.trim() || !formEmail.trim() || !formPhone.trim()) {
      alert("Please fill in all fields.");
      return;
    }

    setIsSubmitting(true);
    const newMemberId = `FIT-${1040 + members.length + 1}`;
    const now = new Date();
    const dateFormatted = now.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });

    const newMember: Member = {
      id: newMemberId,
      name: formName.trim(),
      email: formEmail.trim(),
      phone: formPhone.trim(),
      program: formProgram,
      time_slot: "Morning (06:00 - 09:00)",
      tier: "Pro Member",
      branch: "Pune - Koregaon Park (Flagship)",
      joined_at: dateFormatted
    };

    // Post to API (Vercel / Flask)
    try {
      const res = await fetch('/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newMember)
      });
      if (res.ok) {
        const json = await res.json();
        if (json.member) {
          newMember.id = json.member.id;
        }
      }
    } catch (e) {
      // Fallback
    }

    setMembers(prev => [newMember, ...prev]);
    setIsSubmitting(false);
    setSubmitSuccess(`Thank you for joining our gym, ${newMember.name}! Pass ID ${newMember.id} generated.`);
    setActivePassMember(newMember);

    // Reset inputs
    setFormName('');
    setFormEmail('');
    setFormPhone('');

    setTimeout(() => {
      setSubmitSuccess(null);
    }, 6000);
  };

  // 1-Click Delete Member
  const handleDeleteMember = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm(`Are you sure you want to permanently delete member ${id}?`)) return;

    try {
      await fetch(`/api/members/${id}`, { method: 'DELETE' });
    } catch (e) {
      // fallback
    }

    setMembers(prev => prev.filter(m => m.id !== id));
    if (activePassMember?.id === id) {
      setActivePassMember(null);
    }
  };

  // CSV Export
  const handleExportCSV = () => {
    const headers = ["joined_at", "name", "email", "phone", "program", "id"];
    const rows = members.map(m => [
      `"${m.joined_at}"`,
      `"${m.name}"`,
      `"${m.email}"`,
      `"${m.phone}"`,
      `"${m.program}"`,
      `"${m.id}"`
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `members.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filtered members
  const filteredMembers = useMemo(() => {
    return members.filter(m => {
      const matchesSearch =
        m.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        m.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        m.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        m.phone.includes(searchTerm);

      const matchesBranch = selectedBranchFilter === 'ALL' || m.branch.includes(selectedBranchFilter);
      return matchesSearch && matchesBranch;
    });
  }, [members, searchTerm, selectedBranchFilter]);

  return (
    <div className="min-h-screen bg-[#111111] text-white flex flex-col font-sans selection:bg-[#ffa500] selection:text-black">


      {/* Modern Black Header Navbar */}
      <header className="sticky top-0 z-40 bg-[#000000]/95 backdrop-blur-md border-b border-[#222222]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-[#ffa500] flex items-center justify-center text-black font-black text-sm shadow-md">
              FG
            </div>
            <div>
              <div className="font-display font-black text-2xl tracking-wider text-white uppercase leading-none">
                Fitness Gym
              </div>
              <div className="text-[10px] text-[#ffa500] font-bold tracking-widest uppercase">
                High-Performance Training Club
              </div>
            </div>
          </div>

          <nav className="flex flex-wrap items-center justify-center gap-6 text-sm font-semibold text-white">
            <a href="#home" className="hover:text-[#ffa500] transition-colors">Home</a>
            <a href="#programs" className="hover:text-[#ffa500] transition-colors">Programs</a>
            <a href="#services" className="hover:text-[#ffa500] transition-colors">Services</a>
            <a href="#reviews" className="hover:text-[#ffa500] transition-colors">Reviews</a>
            <a href="#about" className="hover:text-[#ffa500] transition-colors">About</a>
            <a href="#contact" className="hover:text-[#ffa500] transition-colors">Contact</a>
          </nav>

          <a
            href="#contact"
            className="bg-[#ffa500] hover:bg-[#e69500] text-black font-bold px-5 py-2 rounded text-xs uppercase tracking-wider transition-all shadow-md"
          >
            Join Now
          </a>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="relative bg-[#1c1c1c] py-24 sm:py-32 border-b border-[#222222] text-center overflow-hidden">
        {/* Subtle orange ambient glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[300px] bg-[#ffa500]/10 blur-[130px] pointer-events-none rounded-full" />

        <div className="max-w-4xl mx-auto px-4 relative z-10 space-y-5">
          <span className="inline-block bg-[#ffa500]/15 text-[#ffa500] border border-[#ffa500]/30 px-3.5 py-1 rounded-full text-xs font-bold uppercase tracking-widest">
            Best Gym Training in Your City
          </span>

          <h1 className="font-display text-4xl sm:text-6xl md:text-7xl font-black uppercase text-white tracking-tight leading-tight">
            Build Your <span className="text-[#ffa500]">Dream Body</span>
          </h1>

          <p className="text-[#cccccc] text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
            World-class strength equipment, Olympic power racks, certified trainers, and structured Desi sports nutrition plans.
          </p>

          <div className="pt-4 flex flex-wrap justify-center items-center gap-4">
            <a
              href="#contact"
              className="bg-[#ffa500] hover:bg-[#e69500] text-black font-extrabold text-sm uppercase px-8 py-3.5 rounded transition-all shadow-lg hover:scale-105 active:scale-95"
            >
              Join Now
            </a>
            <a
              href="#programs"
              className="bg-[#222222] hover:bg-[#333333] border border-[#333333] text-white font-bold text-sm uppercase px-6 py-3.5 rounded transition-all"
            >
              Explore Programs
            </a>
          </div>
        </div>
      </section>

      {/* Programs Section with Expandable Cards */}
      <section id="programs" className="py-20 border-b border-[#222222] bg-[#111111]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-2">
            <span className="text-xs font-bold text-[#ffa500] uppercase tracking-widest">
              Signature Disciplines
            </span>
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold uppercase text-white">
              Our Training Programs
            </h2>
            <p className="text-[#cccccc] text-sm">
              Click "Learn More" on any card to view detailed training protocols.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {PROGRAMS_DATA.map(prog => {
              const isExpanded = expandedPrograms[prog.id];
              return (
                <div
                  key={prog.id}
                  className="bg-[#222222] border border-[#333333] hover:border-[#ffa500]/50 rounded-xl p-6 flex flex-col justify-between transition-all duration-300 shadow-lg"
                >
                  <div className="space-y-3">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-[#ffa500] bg-[#ffa500]/10 px-2 py-0.5 rounded border border-[#ffa500]/20">
                      {prog.tag}
                    </span>
                    <h3 className="font-display text-2xl font-bold uppercase text-white mt-1">
                      {prog.title}
                    </h3>
                    <p className="text-[#cccccc] text-xs leading-relaxed">
                      {prog.desc}
                    </p>

                    {/* Accordion Expandable Section */}
                    {isExpanded && (
                      <div className="p-3.5 bg-[#181818] rounded-lg border border-[#333333] text-xs text-[#ffffff] mt-3 animate-fade-in leading-relaxed">
                        <strong className="text-[#ffa500] block mb-1">Program Details:</strong>
                        {prog.more}
                      </div>
                    )}
                  </div>

                  <div className="pt-6">
                    <button
                      onClick={() => toggleProgram(prog.id)}
                      className={`w-full font-bold text-xs uppercase py-2.5 px-4 rounded transition-colors flex items-center justify-center gap-1.5 ${
                        isExpanded
                          ? 'bg-[#333333] text-white hover:bg-[#444444]'
                          : 'bg-[#ffa500] text-black hover:bg-[#e69500]'
                      }`}
                    >
                      <span>{isExpanded ? '▲ Hide Info' : 'Learn More'}</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Services Section with Expandable Cards */}
      <section id="services" className="py-20 border-b border-[#222222] bg-[#161616]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-2">
            <span className="text-xs font-bold text-[#ffa500] uppercase tracking-widest">
              Premium Amenities
            </span>
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold uppercase text-white">
              Our Services
            </h2>
            <p className="text-[#cccccc] text-sm">
              Comprehensive athletic development tailored to your lifestyle.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {SERVICES_DATA.map(serv => {
              const isExpanded = expandedServices[serv.id];
              return (
                <div
                  key={serv.id}
                  className="bg-[#222222] border border-[#333333] hover:border-[#ffa500]/50 rounded-xl p-6 flex flex-col justify-between transition-all duration-300 shadow-lg"
                >
                  <div className="space-y-3">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-[#ffa500] bg-[#ffa500]/10 px-2 py-0.5 rounded border border-[#ffa500]/20">
                      {serv.badge}
                    </span>
                    <h3 className="font-display text-2xl font-bold uppercase text-white mt-1">
                      {serv.title}
                    </h3>
                    <p className="text-[#cccccc] text-xs leading-relaxed">
                      {serv.desc}
                    </p>

                    {/* Accordion Expandable Section */}
                    {isExpanded && (
                      <div className="p-3.5 bg-[#181818] rounded-lg border border-[#333333] text-xs text-[#ffffff] mt-3 animate-fade-in leading-relaxed">
                        <strong className="text-[#ffa500] block mb-1">Service Overview:</strong>
                        {serv.more}
                      </div>
                    )}
                  </div>

                  <div className="pt-6">
                    <button
                      onClick={() => toggleService(serv.id)}
                      className={`w-full font-bold text-xs uppercase py-2.5 px-4 rounded transition-colors flex items-center justify-center gap-1.5 ${
                        isExpanded
                          ? 'bg-[#333333] text-white hover:bg-[#444444]'
                          : 'bg-[#ffa500] text-black hover:bg-[#e69500]'
                      }`}
                    >
                      <span>{isExpanded ? '▲ Hide Details' : 'Details'}</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Member Reviews with Circular Avatars */}
      <section id="reviews" className="py-20 border-b border-[#222222] bg-[#000000]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-2">
            <span className="text-xs font-bold text-[#ffa500] uppercase tracking-widest">
              Verified Athletes
            </span>
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold uppercase text-white">
              Member Reviews
            </h2>
            <p className="text-[#cccccc] text-sm">
              Real results from dedicated members training at our facilities.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {REVIEWS_DATA.map(rev => {
              const isExpanded = expandedReviews[rev.id];
              return (
                <div
                  key={rev.id}
                  className="bg-[#222222] border border-[#333333] hover:border-[#ffa500]/50 rounded-xl p-6 flex flex-col justify-between items-center text-center transition-all duration-300 shadow-lg"
                >
                  <div className="space-y-3 w-full flex flex-col items-center">
                    {/* Circle Letter Avatar from Python Tkinter Canvas */}
                    <div className="w-18 h-18 rounded-full bg-[#ffa500] border-2 border-[#ffb733] flex items-center justify-center text-white font-extrabold text-3xl shadow-md my-2">
                      {rev.avatar}
                    </div>

                    <p className="text-white text-sm italic font-medium">
                      {rev.quote}
                    </p>

                    <div className="font-bold text-sm text-[#ffa500]">
                      - {rev.name}
                    </div>

                    <div className="text-[11px] text-[#999999]">
                      {rev.branch}
                    </div>

                    {/* Accordion Expandable Section */}
                    {isExpanded && (
                      <div className="p-3.5 bg-[#181818] rounded-lg border border-[#333333] text-xs text-[#ffffff] mt-3 animate-fade-in leading-relaxed text-left w-full">
                        <strong className="text-[#ffa500] block mb-1">Athlete Journey:</strong>
                        {rev.more}
                      </div>
                    )}
                  </div>

                  <div className="pt-6 w-full">
                    <button
                      onClick={() => toggleReview(rev.id)}
                      className={`w-full font-bold text-xs uppercase py-2.5 px-4 rounded transition-colors flex items-center justify-center gap-1.5 ${
                        isExpanded
                          ? 'bg-[#333333] text-white hover:bg-[#444444]'
                          : 'bg-[#ffa500] text-black hover:bg-[#e69500]'
                      }`}
                    >
                      <span>{isExpanded ? '▲ Close Review' : 'Read More'}</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* About Our Gym Section */}
      <section id="about" className="py-20 border-b border-[#222222] bg-[#111111] text-center">
        <div className="max-w-4xl mx-auto px-4 space-y-6">
          <span className="text-xs font-bold text-[#ffa500] uppercase tracking-widest">
            Who We Are
          </span>
          <h2 className="font-display text-3xl sm:text-4xl font-extrabold uppercase text-white">
            About Our Gym
          </h2>

          <p className="text-[#cccccc] text-base sm:text-lg leading-relaxed max-w-2xl mx-auto">
            Our gym provides world class training with modern equipment and certified trainers. Our mission is to make people fit and healthy.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6">
            <div className="p-5 bg-[#1c1c1c] border border-[#2e2e2e] rounded-xl">
              <div className="font-display text-3xl font-extrabold text-[#ffa500]">1,200+</div>
              <div className="text-xs text-[#aaaaaa] mt-1 font-semibold uppercase">Active Athletes</div>
            </div>
            <div className="p-5 bg-[#1c1c1c] border border-[#2e2e2e] rounded-xl">
              <div className="font-display text-3xl font-extrabold text-white">60 KG</div>
              <div className="text-xs text-[#aaaaaa] mt-1 font-semibold uppercase">Olympic Dumbbells</div>
            </div>
            <div className="p-5 bg-[#1c1c1c] border border-[#2e2e2e] rounded-xl">
              <div className="font-display text-3xl font-extrabold text-[#ffa500]">06:00 - 22:00</div>
              <div className="text-xs text-[#aaaaaa] mt-1 font-semibold uppercase">Daily Hours</div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section: Join Our Gym & CSV Registry */}
      <section id="contact" className="py-20 border-b border-[#222222] bg-[#161616]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-2">
            <span className="text-xs font-bold text-[#ffa500] uppercase tracking-widest">
              Registration & Database
            </span>
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold uppercase text-white">
              Join Our Gym
            </h2>
            <p className="text-[#cccccc] text-sm">
              Register below to generate your digital membership pass and sync with <code className="text-[#ffa500]">members.csv</code>.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Join Gym Form (Matching Tkinter inputs) */}
            <div className="lg:col-span-5 bg-[#222222] border border-[#333333] rounded-xl p-6 sm:p-7 shadow-xl">
              <h3 className="font-display text-xl font-bold uppercase text-white pb-3 border-b border-[#333333]">
                Member Registration
              </h3>

              {submitSuccess && (
                <div className="mt-4 p-3 bg-emerald-500/20 border border-emerald-500/40 rounded-lg text-xs text-emerald-300 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>{submitSuccess}</span>
                </div>
              )}

              <form onSubmit={handleRegister} className="mt-4 space-y-4 text-xs">
                <div>
                  <label className="block text-[#cccccc] font-semibold mb-1">Your Name</label>
                  <input
                    type="text"
                    required
                    value={formName}
                    onChange={e => setFormName(e.target.value)}
                    placeholder="Enter athlete full name..."
                    className="w-full bg-[#181818] border border-[#333333] rounded px-3 py-2.5 text-white placeholder-[#777777] focus:outline-none focus:border-[#ffa500]"
                  />
                </div>

                <div>
                  <label className="block text-[#cccccc] font-semibold mb-1">Your Email</label>
                  <input
                    type="email"
                    required
                    value={formEmail}
                    onChange={e => setFormEmail(e.target.value)}
                    placeholder="name@example.com"
                    className="w-full bg-[#181818] border border-[#333333] rounded px-3 py-2.5 text-white placeholder-[#777777] focus:outline-none focus:border-[#ffa500]"
                  />
                </div>

                <div>
                  <label className="block text-[#cccccc] font-semibold mb-1">Phone Number</label>
                  <input
                    type="text"
                    required
                    value={formPhone}
                    onChange={e => setFormPhone(e.target.value)}
                    placeholder="+91 98201 00000"
                    className="w-full bg-[#181818] border border-[#333333] rounded px-3 py-2.5 text-white placeholder-[#777777] focus:outline-none focus:border-[#ffa500]"
                  />
                </div>

                <div>
                  <label className="block text-[#cccccc] font-semibold mb-1">Select Program</label>
                  <select
                    value={formProgram}
                    onChange={e => setFormProgram(e.target.value)}
                    className="w-full bg-[#181818] border border-[#333333] rounded px-3 py-2.5 text-white focus:outline-none focus:border-[#ffa500]"
                  >
                    <option value="Weight Training">Weight Training</option>
                    <option value="Cardio Training">Cardio Training</option>
                    <option value="Yoga & Mobility">Yoga & Mobility</option>
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full mt-2 bg-[#ffa500] hover:bg-[#e69500] text-black font-extrabold py-3 rounded uppercase tracking-wider text-xs transition-all shadow-md disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {isSubmitting ? 'Registering...' : 'Join Gym'}
                </button>
              </form>
            </div>

            {/* Live Database Viewer & CSV Export */}
            <div className="lg:col-span-7 bg-[#222222] border border-[#333333] rounded-xl p-6 shadow-xl flex flex-col">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#333333]">
                <div>
                  <h3 className="font-display text-xl font-bold uppercase text-white">
                    Registered Athletes (members.csv)
                  </h3>
                  <p className="text-[11px] text-[#aaaaaa]">
                    {filteredMembers.length} records in active memory & CSV
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={handleExportCSV}
                    className="bg-[#333333] hover:bg-[#444444] text-white px-3 py-1.5 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors border border-[#444444]"
                  >
                    <Download className="w-3.5 h-3.5 text-[#ffa500]" />
                    <span>Download CSV</span>
                  </button>
                </div>
              </div>

              {/* Search */}
              <div className="py-3">
                <div className="relative">
                  <Search className="w-4 h-4 text-[#777777] absolute left-3 top-3 pointer-events-none" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                    placeholder="Search members by name, ID, or phone..."
                    className="w-full bg-[#181818] border border-[#333333] rounded pl-9 pr-3 py-2 text-xs text-white placeholder-[#777777] focus:outline-none focus:border-[#ffa500]"
                  />
                </div>
              </div>

              {/* Members List */}
              <div className="space-y-2 max-h-[360px] overflow-y-auto pr-1">
                {filteredMembers.length === 0 ? (
                  <div className="p-8 text-center text-[#777777] text-xs bg-[#181818] rounded border border-[#333333]">
                    No member records found.
                  </div>
                ) : (
                  filteredMembers.map(member => (
                    <div
                      key={member.id}
                      onClick={() => setActivePassMember(member)}
                      className="p-3 bg-[#181818] hover:bg-[#252525] border border-[#333333] hover:border-[#ffa500]/50 rounded-lg flex items-center justify-between gap-3 cursor-pointer transition-all"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="w-8 h-8 rounded-full bg-[#ffa500] text-black font-extrabold text-xs flex items-center justify-center shrink-0">
                          {member.name.charAt(0).toUpperCase()}
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-white text-xs sm:text-sm truncate">
                              {member.name}
                            </span>
                            <span className="text-[10px] bg-[#333333] text-[#ffa500] px-1.5 py-0.5 rounded font-mono">
                              {member.id}
                            </span>
                          </div>
                          <div className="text-[11px] text-[#aaaaaa] truncate">
                            {member.program} • {member.phone}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <button
                          onClick={e => {
                            e.stopPropagation();
                            setActivePassMember(member);
                          }}
                          className="px-2.5 py-1 rounded bg-[#333333] hover:bg-[#ffa500] hover:text-black text-white text-[11px] font-semibold transition-colors"
                        >
                          Pass
                        </button>
                        <button
                          onClick={e => handleDeleteMember(member.id, e)}
                          title="Delete Member Record"
                          className="w-7 h-7 rounded bg-rose-500/10 hover:bg-rose-500/25 text-rose-400 flex items-center justify-center transition-colors"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Digital Pass Modal */}
      {activePassMember && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm animate-fade-in">
          <div className="bg-[#1c1c1c] border-2 border-[#ffa500] rounded-xl max-w-md w-full p-6 shadow-2xl relative">
            <button
              onClick={() => setActivePassMember(null)}
              className="absolute top-4 right-4 text-[#888888] hover:text-white p-1 rounded bg-[#2e2e2e]"
            >
              ✕
            </button>

            <div className="text-center pb-4 border-b border-[#333333] space-y-1">
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#ffa500] font-bold">
                Fitness Gym Official Member Card
              </span>
              <h3 className="font-display text-2xl font-bold uppercase text-white">
                Digital Gym Pass
              </h3>
            </div>

            <div className="py-6 space-y-4">
              <div className="p-4 rounded-xl bg-[#111111] border border-[#333333] text-center space-y-2">
                <div className="w-16 h-16 mx-auto rounded-full bg-[#ffa500] text-black font-extrabold text-2xl flex items-center justify-center border-2 border-white">
                  {activePassMember.name.charAt(0).toUpperCase()}
                </div>
                <h4 className="font-display text-2xl font-extrabold text-white uppercase">
                  {activePassMember.name}
                </h4>
                <div className="font-mono text-[#ffa500] font-bold text-sm bg-black py-1 px-3 rounded inline-block border border-[#ffa500]/30">
                  {activePassMember.id}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2.5 bg-[#252525] rounded border border-[#333333]">
                  <span className="text-[#888888] block text-[10px]">Program</span>
                  <span className="font-semibold text-white">{activePassMember.program}</span>
                </div>
                <div className="p-2.5 bg-[#252525] rounded border border-[#333333]">
                  <span className="text-[#888888] block text-[10px]">Tier</span>
                  <span className="font-semibold text-[#ffa500]">{activePassMember.tier}</span>
                </div>
                <div className="p-2.5 bg-[#252525] rounded border border-[#333333]">
                  <span className="text-[#888888] block text-[10px]">Phone</span>
                  <span className="font-semibold text-white">{activePassMember.phone}</span>
                </div>
                <div className="p-2.5 bg-[#252525] rounded border border-[#333333]">
                  <span className="text-[#888888] block text-[10px]">Club Branch</span>
                  <span className="font-semibold text-white truncate block">
                    {activePassMember.branch.split(' - ')[1] || activePassMember.branch}
                  </span>
                </div>
              </div>

              <div className="text-[11px] text-[#888888] text-center pt-2">
                Joined: {activePassMember.joined_at}
              </div>
            </div>

            <button
              onClick={() => setActivePassMember(null)}
              className="w-full bg-[#ffa500] hover:bg-[#e69500] text-black font-bold py-2.5 rounded text-xs uppercase tracking-wider transition-colors"
            >
              Close Pass
            </button>
          </div>
        </div>
      )}

      {/* Python Script Modal (Direct Access to gym_app.py) */}
      {showPythonScriptModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
          <div className="bg-[#141414] border border-[#333333] rounded-xl max-w-3xl w-full p-6 shadow-2xl relative max-h-[90vh] flex flex-col">
            <button
              onClick={() => setShowPythonScriptModal(false)}
              className="absolute top-4 right-4 text-[#888888] hover:text-white p-1 rounded bg-[#2e2e2e]"
            >
              ✕
            </button>

            <div className="flex items-center gap-3 pb-4 border-b border-[#333333]">
              <div className="w-10 h-10 rounded-lg bg-[#ffa500]/20 text-[#ffa500] flex items-center justify-center">
                <Monitor className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-display text-2xl font-bold uppercase text-white">
                  Python Desktop App (`gym_app.py`)
                </h3>
                <p className="text-xs text-[#aaaaaa]">
                  Modernized Tkinter frontend with dark aesthetic, accordion cards, and CSV persistence.
                </p>
              </div>
            </div>

            <div className="py-4 space-y-4 overflow-y-auto flex-1 text-xs text-[#cccccc]">
              <div className="p-3 bg-[#1e1e1e] rounded border border-[#333333] space-y-1.5">
                <strong className="text-white block">How to run on your computer:</strong>
                <div className="p-2 bg-black rounded font-mono text-[#ffa500] flex justify-between items-center">
                  <span>python gym_app.py</span>
                  <button
                    onClick={() => handleCopy('python gym_app.py', 'pycmd')}
                    className="text-[#888888] hover:text-white"
                  >
                    {copiedKey === 'pycmd' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                </div>
                <span className="text-[11px] text-[#888888] block">
                  Zero external pip packages required! Works with standard Python 3.8+ on Windows, macOS, and Linux.
                </span>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-white">Features in the modernized Python GUI:</span>
                  <button
                    onClick={() => handleCopy('# gym_app.py is available in project root', 'copycode')}
                    className="text-[#ffa500] hover:underline text-[11px]"
                  >
                    File saved in project root as gym_app.py
                  </button>
                </div>
                <ul className="list-disc pl-5 space-y-1 text-[11px] text-[#aaaaaa]">
                  <li>Modern dark palette (<code className="text-[#ffa500]">#111111</code>, <code className="text-[#ffa500]">#1c1c1c</code>, and orange <code className="text-[#ffa500]">#ffa500</code> accent).</li>
                  <li>Smooth interactive accordion toggle cards for Programs, Services, and Reviews.</li>
                  <li>Canvas-rendered high-contrast circular letter avatars for testimonials.</li>
                  <li>Live Member Registry with integrated Treeview table and <code className="text-[#ffa500]">members.csv</code> auto-persistence.</li>
                  <li>1-click record removal and refresh directly inside the desktop interface.</li>
                </ul>
              </div>
            </div>

            <div className="pt-3 border-t border-[#333333]">
              <button
                onClick={() => setShowPythonScriptModal(false)}
                className="w-full bg-[#ffa500] hover:bg-[#e69500] text-black font-bold py-2.5 rounded text-xs uppercase tracking-wider transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Vercel Deployment Hub Modal */}
      {showVercelModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
          <div className="bg-[#141414] border border-[#ffa500]/40 rounded-xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowVercelModal(false)}
              className="absolute top-4 right-4 text-[#888888] hover:text-white p-1 rounded bg-[#2e2e2e]"
            >
              ✕
            </button>

            <div className="flex items-center gap-3 pb-4 border-b border-[#333333]">
              <div className="w-10 h-10 rounded-lg bg-[#ffa500]/20 text-[#ffa500] flex items-center justify-center">
                <Terminal className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-display text-2xl font-bold uppercase text-white">
                  Vercel Deployment Hub
                </h3>
                <p className="text-xs text-[#aaaaaa]">
                  Full-Stack Architecture: React (Vite SPA) + Python Serverless API (<code className="text-[#ffa500]">api/index.py</code>)
                </p>
              </div>
            </div>

            <div className="py-5 space-y-5 text-xs text-[#cccccc]">
              {/* Commands */}
              <div className="space-y-2">
                <span className="font-bold text-white uppercase text-[11px] tracking-wider">
                  Deploy to Vercel in 1 Minute
                </span>
                <div className="p-3 bg-black rounded font-mono text-[11px] space-y-2 border border-[#333333]">
                  <div className="text-[#777777]"># 1. Install Vercel CLI</div>
                  <div className="flex justify-between text-[#ffa500] bg-[#181818] p-1.5 rounded">
                    <span>npm i -g vercel</span>
                    <button onClick={() => handleCopy('npm i -g vercel', 'v1')} className="text-[#888888] hover:text-white">
                      {copiedKey === 'v1' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>

                  <div className="text-[#777777] pt-1"># 2. Deploy to Production</div>
                  <div className="flex justify-between text-[#ffa500] bg-[#181818] p-1.5 rounded">
                    <span>vercel --prod</span>
                    <button onClick={() => handleCopy('vercel --prod', 'v2')} className="text-[#888888] hover:text-white">
                      {copiedKey === 'v2' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                </div>
              </div>

              {/* Status */}
              <div className="p-3 bg-[#1e1e1e] rounded border border-[#333333] flex items-center justify-between">
                <div>
                  <span className="text-[11px] text-[#888888] block">API Health Probe:</span>
                  <span className="text-xs font-mono font-bold text-[#ffa500]">{apiResponseInfo || 'Checking probe...'}</span>
                </div>
                <button
                  onClick={checkApiHealth}
                  className="px-3 py-1 bg-[#333333] hover:bg-[#444444] rounded text-white text-xs font-semibold"
                >
                  Re-test
                </button>
              </div>
            </div>

            <button
              onClick={() => setShowVercelModal(false)}
              className="w-full bg-[#ffa500] hover:bg-[#e69500] text-black font-bold py-2.5 rounded text-xs uppercase tracking-wider transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Modern Black Footer */}
      <footer className="mt-auto bg-[#000000] border-t border-[#222222] py-8 text-xs text-[#888888] text-center">
        <div className="max-w-7xl mx-auto px-4 space-y-2">
          <p className="text-white font-medium">
            © 2026 Fitness Gym Website
          </p>
        </div>
      </footer>
    </div>
  );
}
